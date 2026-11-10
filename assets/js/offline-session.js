/**
 * MCD Offline Mode v8
 * App download UI when:
 *  - opened via /app.html or ?mcd=app (APK)
 *  - or real PWA standalone
 * Hidden on normal Google/browser URL.
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  function markAppMode() {
    try {
      sessionStorage.setItem("mcd_app_mode", "1");
      localStorage.setItem("mcd_app_mode", "1");
    } catch (e) {}
  }

  function isAppMode() {
    try {
      var q = location.search || "";
      var path = location.pathname || "";
      if (/[?&]mcd=app\b/i.test(q) || /\/app\.html$/i.test(path)) {
        markAppMode();
        return true;
      }
      try {
        if (sessionStorage.getItem("mcd_app_mode") === "1") return true;
        if (localStorage.getItem("mcd_app_mode") === "1") return true;
      } catch (e1) {}
      if (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) return true;
      if (typeof navigator.standalone === "boolean" && navigator.standalone === true) return true;
    } catch (e) {}
    return false;
  }

  function stripOfflineUI() {
    ["mcd-offline-nav", "mcd-offline-modal", "mcd-offline-fab", "mcd-page-save"].forEach(function (id) {
      var el = document.getElementById(id);
      if (el && el.parentNode) try { el.parentNode.removeChild(el); } catch (e) {}
    });
  }

  /* Google / normal browser without app flag */
  if (!isAppMode()) {
    try {
      sessionStorage.removeItem("mcd_app_mode");
      localStorage.removeItem("mcd_app_mode");
      localStorage.removeItem("mcd_is_app");
    } catch (eClr) {}
    stripOfflineUI();
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", stripOfflineUI);
    setTimeout(stripOfflineUI, 500);
    setTimeout(stripOfflineUI, 2000);
    return;
  }

  var CACHE_NAME = "mcd-offline-v7";
  var DB_NAME = "mcd_offline_db_v7";
  var DB_VER = 1;
  var MANIFEST_VERSION = "2026-11-10-v7";
  var MAX_ATTEMPTS = 3;
  var CONSENT_KEY = "mcd_offline_consent_v1";
  var DONE_KEY = "mcd_offline_done_v1";

  var SCOPE_BASE = (function () {
    var p = location.pathname || "/";
    if (p.indexOf("/programer") === 0) return "/programer/";
    return "/";
  })();

  var isMobile = false;
  try {
    isMobile =
      window.matchMedia("(max-width:900px)").matches ||
      navigator.maxTouchPoints > 1 ||
      /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent || "");
  } catch (e) {}

  var STATIC_ASSETS = [
    "index.html", "app.html", "404.html", "sw.js", "robots.txt", "sitemap.xml", "offline-manifest-meta.json",
    "site.webmanifest", "assets/css/main.css", "assets/js/boot-loader.js", "assets/js/app.js",
    "assets/js/home.js", "assets/js/mcd-motion.js", "assets/js/offline-session.js",
    "assets/js/search.js", "assets/js/exercises.js", "assets/js/tamrin-filter.js",
    "assets/img/favicon.svg", "assets/img/og-default.svg"
  ];

  var state = {
    total: 0, cached: 0, failed: 0, pending: 0,
    running: false, resources: [], byPath: {},
    stopFlag: false, packReady: false, lastSpeed: 0
  };

  function absUrl(rel) {
    try { return new URL(String(rel).replace(/^\//, ""), location.origin + SCOPE_BASE).href; }
    catch (e) { return location.origin + SCOPE_BASE + String(rel).replace(/^\//, ""); }
  }
  function classify(p) {
    var pl = String(p).toLowerCase();
    if (/\.html?$/.test(pl)) return "html";
    if (/\.css$/.test(pl)) return "css";
    if (/\.js$/.test(pl)) return "js";
    if (/\.(png|jpe?g|webp|gif|svg|ico)$/.test(pl)) return "image";
    if (/\.(xml|txt|json|webmanifest)$/.test(pl)) return "data";
    return "other";
  }
  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function openDb() {
    return new Promise(function (resolve, reject) {
      if (!window.indexedDB) { reject(new Error("no idb")); return; }
      var req = indexedDB.open(DB_NAME, DB_VER);
      req.onupgradeneeded = function () {
        var db = req.result;
        if (!db.objectStoreNames.contains("files")) db.createObjectStore("files", { keyPath: "path" });
        if (!db.objectStoreNames.contains("meta")) db.createObjectStore("meta", { keyPath: "key" });
      };
      req.onsuccess = function () { resolve(req.result); };
      req.onerror = function () { reject(req.error); };
    });
  }
  function idbGetAll(store) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, "readonly");
        var req = tx.objectStore(store).getAll();
        req.onsuccess = function () { resolve(req.result || []); };
        req.onerror = function () { reject(req.error); };
      });
    });
  }
  function idbPut(store, value) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, "readwrite");
        tx.objectStore(store).put(value);
        tx.oncomplete = function () { resolve(); };
        tx.onerror = function () { reject(tx.error); };
      });
    });
  }
  function idbGetMeta(key) {
    return openDb().then(function (db) {
      return new Promise(function (resolve) {
        var tx = db.transaction("meta", "readonly");
        var req = tx.objectStore("meta").get(key);
        req.onsuccess = function () { resolve(req.result ? req.result.value : null); };
        req.onerror = function () { resolve(null); };
      });
    });
  }
  function idbSetMeta(key, value) { return idbPut("meta", { key: key, value: value }); }

  function profileNetwork() {
    var level = "mid";
    try {
      var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (c) {
        if (c.saveData) return { concurrency: 1, pauseMs: 800 };
        var t = String(c.effectiveType || "").toLowerCase();
        if (t === "slow-2g" || t === "2g") level = "very-slow";
        else if (t === "3g") level = "slow";
        else if (t === "4g") level = "fast";
      }
    } catch (e) {}
    if (isMobile && level === "fast") level = "mid";
    return {
      "very-slow": { concurrency: 1, pauseMs: 1200 },
      slow: { concurrency: 2, pauseMs: 500 },
      mid: { concurrency: isMobile ? 2 : 3, pauseMs: isMobile ? 250 : 120 },
      fast: { concurrency: isMobile ? 3 : 5, pauseMs: isMobile ? 100 : 40 }
    }[level] || { concurrency: 2, pauseMs: 200 };
  }

  function injectUI() {
    if (document.getElementById("mcd-offline-nav")) return true;
    var host = document.querySelector("header nav") || document.querySelector("header") || document.body;
    if (!host) return false;

    var wrap = document.createElement("div");
    wrap.id = "mcd-offline-nav";
    wrap.setAttribute("dir", "rtl");
    wrap.style.cssText =
      "display:inline-flex;align-items:center;gap:6px;margin:4px;padding:4px 10px;border-radius:999px;" +
      "border:1px solid #238636;background:#0d1117;font-family:system-ui,sans-serif;z-index:99990;white-space:nowrap";

    var title = document.createElement("span");
    title.textContent = "حالت آفلاین";
    title.style.cssText = "font-size:11px;font-weight:700;color:#00e676";

    var status = document.createElement("span");
    status.id = "mcd-offline-status";
    status.style.cssText = "font-size:10px;color:#8b949e";
    status.textContent = "آماده";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = "mcd-offline-open";
    btn.textContent = "دانلود";
    btn.style.cssText =
      "background:#238636;color:#fff;border:0;border-radius:8px;padding:4px 12px;" +
      "font-size:11px;cursor:pointer;font-weight:700";

    wrap.appendChild(title);
    wrap.appendChild(status);
    wrap.appendChild(btn);
    host.appendChild(wrap);

    btn.onclick = function () { openModal(); };
    updateStatusBadge();
    return true;
  }

  function ensureUI() {
    if (injectUI()) return;
    var n = 0;
    var t = setInterval(function () {
      n++;
      if (injectUI() || n > 50) clearInterval(t);
    }, 200);
  }

  function updateStatusBadge() {
    var el = document.getElementById("mcd-offline-status");
    if (!el) return;
    if (state.running) el.textContent = "در حال دانلود";
    else if (state.packReady && state.failed === 0) el.textContent = "آماده آفلاین";
    else if (state.failed > 0) el.textContent = "ناقص";
    else if (state.cached > 0) el.textContent = state.cached + "/" + state.total;
    else el.textContent = "آماده";
  }

  var modal = null;
  function ensureModal() {
    if (modal) return modal;
    modal = document.createElement("div");
    modal.id = "mcd-offline-modal";
    modal.setAttribute("dir", "rtl");
    modal.style.cssText =
      "position:fixed;inset:0;z-index:100000;background:rgba(0,0,0,.8);display:none;" +
      "align-items:center;justify-content:center;padding:14px;font-family:system-ui,sans-serif";
    modal.innerHTML =
      '<div style="width:min(460px,100%);max-height:92vh;overflow:auto;background:#0d1117;border:1px solid #238636;border-radius:16px;padding:16px;color:#e6edf3">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">' +
      '<b style="color:#00e676;font-size:16px">دانلود کامل سایت برای استفاده آفلاین</b>' +
      '<button type="button" id="mcd-modal-x" style="background:transparent;border:0;color:#8b949e;font-size:20px;cursor:pointer">×</button></div>' +
      '<p style="margin:0 0 10px;line-height:1.75;color:#c9d1d9;font-size:12.5px">با ذخیره آفلاین می‌توانید درس‌ها را بدون اینترنت بخوانید. وقتی آنلاین هستید سایت از نسخه به‌روز شبکه بارگذاری می‌شود.</p>' +
      '<div id="mcd-modal-meta" style="font-size:11px;color:#8b949e;margin-bottom:8px">…</div>' +
      '<div id="mcd-modal-status" style="color:#00e676;font-size:12px;margin-bottom:6px">آماده</div>' +
      '<div style="height:10px;background:#21262d;border-radius:99px;overflow:hidden;margin-bottom:6px">' +
      '<div id="mcd-modal-bar" style="height:100%;width:0%;background:#00e676;transition:width .2s"></div></div>' +
      '<div id="mcd-modal-nums" style="color:#8b949e;font-size:11px;margin-bottom:12px">۰ / ۰</div>' +
      '<div style="display:flex;gap:6px;flex-wrap:wrap">' +
      '<button type="button" id="mcd-modal-start" style="flex:1;min-width:110px;background:#238636;color:#fff;border:0;border-radius:10px;padding:10px;cursor:pointer;font-weight:700">شروع دانلود</button>' +
      '<button type="button" id="mcd-modal-pause" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:10px;padding:10px 12px;cursor:pointer">توقف</button>' +
      '<button type="button" id="mcd-modal-resume" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:10px;padding:10px 12px;cursor:pointer">ادامه</button>' +
      '<button type="button" id="mcd-modal-retry" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:10px;padding:10px 12px;cursor:pointer">تلاش مجدد</button></div></div>';
    document.body.appendChild(modal);
    document.getElementById("mcd-modal-x").onclick = function () { modal.style.display = "none"; };
    document.getElementById("mcd-modal-start").onclick = function () { lsSet(CONSENT_KEY, "yes"); startDownload(false); };
    document.getElementById("mcd-modal-pause").onclick = function () {
      state.stopFlag = true; state.running = false; renderProgress("متوقف شد");
    };
    document.getElementById("mcd-modal-resume").onclick = function () { startDownload(false); };
    document.getElementById("mcd-modal-retry").onclick = function () { startDownload(true); };
    return modal;
  }

  function openModal() {
    ensureModal();
    modal.style.display = "flex";
    preparePack(false);
    renderProgress();
  }

  function renderProgress(statusText) {
    ensureModal();
    var pct = state.total ? Math.floor((state.cached / state.total) * 100) : 0;
    var bar = document.getElementById("mcd-modal-bar");
    var nums = document.getElementById("mcd-modal-nums");
    var st = document.getElementById("mcd-modal-status");
    var meta = document.getElementById("mcd-modal-meta");
    if (bar) bar.style.width = pct + "%";
    if (nums) nums.textContent = "ذخیره‌شده: " + state.cached + " / " + state.total + " (" + pct + "٪) · ناموفق: " + state.failed + " · مانده: " + state.pending;
    if (meta) meta.textContent = "نسخه: " + MANIFEST_VERSION + " · فایل‌های شناسایی‌شده: " + state.total;
    if (st) {
      if (statusText) st.textContent = statusText;
      else if (state.running) st.textContent = "در حال دانلود…";
      else if (state.packReady && state.failed === 0) st.textContent = "دانلود شد";
      else if (state.failed > 0) st.textContent = "دانلود ناقص — تلاش مجدد";
      else st.textContent = "آماده برای شروع";
    }
    updateStatusBadge();
  }

  function recount() {
    var c = 0, f = 0, p = 0;
    for (var i = 0; i < state.resources.length; i++) {
      var s = state.resources[i].status;
      if (s === "cached") c++; else if (s === "failed") f++; else p++;
    }
    state.cached = c; state.failed = f; state.pending = p;
  }

  function cacheOneVerified(path) {
    var url = absUrl(path);
    return fetch(url, { credentials: "same-origin", cache: "no-cache" }).then(function (res) {
      if (!res || !res.ok || res.type === "opaque") throw new Error("http");
      return res.blob().then(function (blob) {
        var putRes = new Response(blob, { status: res.status, statusText: res.statusText, headers: res.headers });
        return caches.open(CACHE_NAME).then(function (cache) {
          return cache.put(url, putRes).then(function () {
            return cache.match(url).then(function (m) {
              if (!m) throw new Error("verify");
              return true;
            });
          });
        });
      });
    });
  }

  function pathFromLoc(loc) {
    try {
      var u = new URL(loc); var path = u.pathname || "/";
      if (path.indexOf("/programer/") === 0) path = path.slice("/programer/".length);
      else if (path.indexOf("/programer") === 0) path = path.slice("/programer".length).replace(/^\//, "");
      if (!path || path === "/") return "index.html";
      return path.replace(/^\//, "");
    } catch (e) { return null; }
  }

  function loadManifest() {
    var metaP = fetch(absUrl("offline-manifest-meta.json"), { cache: "no-cache" }).then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; });
    var mapP = fetch(absUrl("sitemap.xml"), { cache: "no-cache" }).then(function (r) { return r.ok ? r.text() : ""; }).then(function (xml) {
      var urls = [], re = /<loc>\s*([^<]+)\s*<\/loc>/gi, m;
      while ((m = re.exec(xml))) urls.push(m[1].trim());
      return urls;
    }).catch(function () { return []; });
    return Promise.all([metaP, mapP]).then(function (pair) {
      var meta = pair[0] || {}, locs = pair[1] || [], seen = {}, resources = [];
      if (meta.version) MANIFEST_VERSION = meta.version;
      if (meta.cacheName) CACHE_NAME = meta.cacheName;
      function add(path) { if (!path || seen[path]) return; seen[path] = 1; resources.push({ p: path, t: classify(path) }); }
      STATIC_ASSETS.forEach(add);
      locs.forEach(function (loc) { var p = pathFromLoc(loc); if (p) add(p); });
      return { version: MANIFEST_VERSION, cacheName: CACHE_NAME, resources: resources };
    });
  }

  function hydrate(manifest) {
    MANIFEST_VERSION = manifest.version || MANIFEST_VERSION;
    if (manifest.cacheName) CACHE_NAME = manifest.cacheName;
    var list = (manifest.resources || []).map(function (r) {
      return { path: r.p || r.path, type: r.t || "other", status: "pending", attempts: 0, error: null };
    });
    state.resources = list; state.total = list.length; state.byPath = {};
    list.forEach(function (it) { state.byPath[it.path] = it; });
    return idbGetAll("files").then(function (rows) {
      (rows || []).forEach(function (row) {
        var item = state.byPath[row.path];
        if (item) {
          item.status = row.status || "pending";
          item.attempts = row.attempts || 0;
          if (item.status === "downloading" || item.status === "retrying") item.status = "pending";
        }
      });
      recount();
      if (state.cached === state.total && state.total > 0 && state.failed === 0) {
        state.packReady = true; lsSet(DONE_KEY, "1");
      }
      return false;
    });
  }

  function persistItem(item) {
    return idbPut("files", { path: item.path, status: item.status, attempts: item.attempts, error: item.error, updatedAt: Date.now() });
  }
  function pickNext(retryOnly) {
    for (var i = 0; i < state.resources.length; i++) {
      var it = state.resources[i];
      if (retryOnly) { if (it.status === "failed" && it.attempts < MAX_ATTEMPTS) return it; }
      else if (it.status === "pending" || it.status === "failed") return it;
    }
    return null;
  }

  function startDownload(retryOnly) {
    if (state.running) return;
    if (!navigator.onLine) { renderProgress("اینترنت ندارید"); return; }
    state.stopFlag = false; state.running = true; lsSet(CONSENT_KEY, "yes");
    renderProgress("در حال دانلود…");
    var profile = profileNetwork();
    if (!state.resources.length) {
      preparePack(false).then(function () { state.running = false; startDownload(retryOnly); });
      return;
    }
    var active = 0, concurrency = profile.concurrency;
    function pump() {
      if (state.stopFlag) { state.running = false; renderProgress("متوقف شد"); return; }
      while (active < concurrency) {
        var item = pickNext(retryOnly);
        if (!item) break;
        active++; item.status = "downloading"; item.attempts += 1; persistItem(item); recount(); renderProgress();
        (function (current) {
          cacheOneVerified(current.path)
            .then(function () { current.status = "cached"; return persistItem(current); })
            .catch(function () { current.status = "failed"; return persistItem(current); })
            .then(function () { active--; recount(); renderProgress(); setTimeout(pump, profile.pauseMs || 0); });
        })(item);
      }
      if (active === 0) {
        state.running = false; recount();
        if (state.cached === state.total && state.failed === 0) {
          state.packReady = true; lsSet(DONE_KEY, "1");
          try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch (eP) {}
          renderProgress("دانلود شد");
        } else if (state.failed > 0) renderProgress("دانلود ناقص — " + state.failed + " ناموفق");
        else renderProgress("آماده");
      }
    }
    pump();
  }

  function preparePack() {
    return loadManifest().then(function (manifest) {
      return hydrate(manifest).then(function () { recount(); renderProgress(); });
    }).catch(function () { renderProgress("خطا در فهرست فایل‌ها"); });
  }

  function injectPageSave() {
    if (document.getElementById("mcd-page-save")) return;
    var path = location.pathname || "/";
    if (path.indexOf("/programer/") === 0) path = path.slice("/programer/".length);
    else if (path.indexOf("/programer") === 0) path = path.slice("/programer".length).replace(/^\//, "");
    if (!path || path === "/") path = "index.html";
    path = path.replace(/^\//, "");
    var btn = document.createElement("button");
    btn.type = "button"; btn.id = "mcd-page-save";
    btn.textContent = "ذخیره این صفحه";
    btn.style.cssText = "position:fixed;bottom:16px;left:16px;z-index:99980;background:#238636;color:#fff;border:0;border-radius:12px;padding:10px 14px;font-size:12px;cursor:pointer;font-family:system-ui,sans-serif";
    btn.onclick = function () {
      if (!navigator.onLine) { alert("برای دانلود باید اینترنت داشته باشید"); return; }
      btn.disabled = true; btn.textContent = "در حال ذخیره…";
      cacheOneVerified(path).then(function () {
        btn.textContent = "ذخیره شد";
        setTimeout(function () { btn.style.display = "none"; }, 1500);
      }).catch(function () { btn.disabled = false; btn.textContent = "خطا — دوباره"; });
    };
    document.body.appendChild(btn);
  }

  function registerSW() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    var swUrl = (SCOPE_BASE + "sw.js").replace(/([^:]\/)\/+/g, "$1");
    return navigator.serviceWorker.register(swUrl, { scope: SCOPE_BASE }).catch(function () { return null; });
  }

  function init() {
    markAppMode();
    ensureUI();
    injectPageSave();
    registerSW().then(function () {
      state.packReady = lsGet(DONE_KEY) === "1";
      updateStatusBadge();
      if (navigator.onLine) preparePack();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
