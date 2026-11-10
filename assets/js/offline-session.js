/**
 * MCD offline — in APK WebView / PWA only. Not in normal Google/browser tabs.
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  function isWebAppMode() {
    try {
      /* 1) لینک اختصاصی APK: .../programer/?mcdapp=1 */
      var q = location.search || "";
      if (/[?&](mcdapp|app)=1\b/i.test(q)) {
        try { localStorage.setItem("mcd_is_app", "1"); } catch (e0) {}
        return true;
      }
      try { if (localStorage.getItem("mcd_is_app") === "1") return true; } catch (e1) {}

      /* 2) Android WebView داخل APKهای لینک‌محور */
      var ua = navigator.userAgent || "";
      if (/;\s*wv\)/i.test(ua) || /\bwv\b/i.test(ua)) return true;

      /* 3) PWA واقعی نصب‌شده */
      if (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) return true;
      if (typeof navigator.standalone === "boolean" && navigator.standalone) return true;
      if (document.referrer && document.referrer.indexOf("android-app://") === 0) return true;
    } catch (e) {}
    return false;
  }

  function stripOfflineUI() {
    try {
      var a = document.getElementById("mcd-offline-nav");
      if (a && a.parentNode) a.parentNode.removeChild(a);
      var b = document.getElementById("mcd-offline-modal");
      if (b && b.parentNode) b.parentNode.removeChild(b);
    } catch (e) {}
  }

  if (!isWebAppMode()) {
    stripOfflineUI();
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", stripOfflineUI);
    setTimeout(stripOfflineUI, 500);
    setTimeout(stripOfflineUI, 2000);
    return;
  }

  var CACHE_NAME = "mcd-offline-v6";
  var DB_NAME = "mcd_offline_db_v6";
  var DB_VER = 1;
  var MANIFEST_VERSION = "2026-11-10-v6";
  var MAX_ATTEMPTS = 3;
  var CONSENT_KEY = "mcd_offline_consent_v1";
  var ENABLED_KEY = "mcd_offline_enabled_v1";
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
    "index.html", "404.html", "sw.js", "robots.txt", "sitemap.xml", "offline-manifest-meta.json",
    "assets/css/main.css", "assets/js/boot-loader.js", "assets/js/app.js", "assets/js/home.js",
    "assets/js/mcd-motion.js", "assets/js/offline-session.js", "assets/js/search.js",
    "assets/js/exercises.js", "assets/js/tamrin-filter.js", "assets/img/favicon.svg", "assets/img/og-default.svg"
  ];

  var state = {
    total: 0, cached: 0, failed: 0, pending: 0, downloading: 0,
    running: false, resources: [], byPath: {}, stopFlag: false,
    consented: false, enabled: false, online: navigator.onLine !== false,
    packReady: false, autoSync: true, userOverride: false
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
    if (/\.(xml|txt|json)$/.test(pl)) return "data";
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
        if (c.saveData) return { concurrency: 0, pauseMs: 0 };
        var t = String(c.effectiveType || "").toLowerCase();
        if (t === "slow-2g" || t === "2g") level = "very-slow";
        else if (t === "3g") level = "slow";
        else if (t === "4g") level = "fast";
      }
    } catch (e) {}
    if (isMobile && level === "fast") level = "mid";
    var map = {
      "very-slow": { concurrency: 1, pauseMs: 1200 },
      slow: { concurrency: 2, pauseMs: 600 },
      mid: { concurrency: isMobile ? 2 : 3, pauseMs: isMobile ? 400 : 200 },
      fast: { concurrency: isMobile ? 3 : 4, pauseMs: isMobile ? 200 : 80 }
    };
    return map[level] || map.mid;
  }

  function findHeaderHost() {
    return document.querySelector("header nav") || document.querySelector("header") || document.body;
  }

  function injectHeaderToggle() {
    if (document.getElementById("mcd-offline-nav")) { updateLeverUI(); return true; }
    var host = findHeaderHost();
    if (!host) return false;
    var wrap = document.createElement("div");
    wrap.id = "mcd-offline-nav";
    wrap.setAttribute("dir", "rtl");
    wrap.style.cssText =
      "display:inline-flex;align-items:center;gap:6px;margin:4px;padding:4px 8px;border-radius:999px;" +
      "border:1px solid #238636;background:#0d1117;user-select:none;white-space:nowrap;z-index:99990";
    var label = document.createElement("span");
    label.id = "mcd-mode-label";
    label.style.cssText = "font-size:11px;font-weight:700;min-width:3.2em;text-align:center;color:#00e676";
    label.textContent = "آنلاین";
    var track = document.createElement("button");
    track.type = "button"; track.id = "mcd-offline-lever";
    track.setAttribute("role", "switch");
    track.style.cssText = "position:relative;width:42px;height:22px;border-radius:999px;border:0;padding:0;cursor:pointer;background:#30363d";
    var knob = document.createElement("span");
    knob.id = "mcd-lever-knob";
    knob.style.cssText = "position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#e6edf3;transition:left .2s";
    track.appendChild(knob);
    var dlBtn = document.createElement("button");
    dlBtn.type = "button"; dlBtn.id = "mcd-download-view-btn";
    dlBtn.textContent = "دانلود";
    dlBtn.style.cssText = "background:#21262d;color:#00e676;border:1px solid #238636;border-radius:8px;padding:3px 8px;font-size:11px;cursor:pointer;font-weight:600";
    wrap.appendChild(label); wrap.appendChild(track); wrap.appendChild(dlBtn);
    host.appendChild(wrap);
    track.addEventListener("click", function (e) {
      e.preventDefault();
      var next = !state.enabled;
      state.userOverride = true;
      if (next) onUserEnableOffline(); else onUserDisableOffline();
      updateLeverUI();
    });
    dlBtn.addEventListener("click", function (e) {
      e.preventDefault();
      openModal();
      if (state.consented && !state.packReady && navigator.onLine) preparePack(false);
    });
    updateLeverUI();
    return true;
  }

  function ensureToggleMounted() {
    if (injectHeaderToggle()) return;
    var tries = 0;
    var t = setInterval(function () {
      tries++;
      if (injectHeaderToggle() || tries > 40) clearInterval(t);
    }, 250);
  }

  function setLeverVisual(on) {
    var track = document.getElementById("mcd-offline-lever");
    var knob = document.getElementById("mcd-lever-knob");
    var label = document.getElementById("mcd-mode-label");
    if (!track || !knob || !label) return;
    if (on) {
      track.style.background = "#238636"; knob.style.left = "22px";
      label.textContent = "آفلاین"; label.style.color = "#f0b429";
    } else {
      track.style.background = "#30363d"; knob.style.left = "2px";
      label.textContent = "آنلاین"; label.style.color = "#00e676";
    }
  }

  function updateLeverUI() {
    if (state.packReady && state.autoSync && !state.userOverride) state.enabled = !state.online;
    setLeverVisual(!!state.enabled);
    if (!state.packReady) {
      var label = document.getElementById("mcd-mode-label");
      if (label) {
        label.textContent = state.online ? "آنلاین" : "آفلاین";
        label.style.color = state.online ? "#00e676" : "#f0b429";
      }
    }
  }

  var modal = null;
  function ensureModal() {
    if (modal) return modal;
    modal = document.createElement("div");
    modal.id = "mcd-offline-modal";
    modal.setAttribute("dir", "rtl");
    modal.style.cssText = "position:fixed;inset:0;z-index:100000;background:rgba(0,0,0,.75);display:none;align-items:center;justify-content:center;padding:16px;font-family:system-ui,sans-serif";
    modal.innerHTML =
      '<div style="width:min(440px,100%);background:#0d1117;border:1px solid #238636;border-radius:16px;padding:18px 16px;color:#e6edf3">' +
      '<div style="display:flex;justify-content:space-between;margin-bottom:10px"><b style="color:#00e676">وضعیت دانلود آفلاین</b>' +
      '<button type="button" id="mcd-modal-x" style="background:transparent;border:0;color:#8b949e;font-size:18px;cursor:pointer">×</button></div>' +
      '<div id="mcd-modal-status" style="color:#8b949e;font-size:12px;margin-bottom:6px">آماده</div>' +
      '<div style="height:8px;background:#21262d;border-radius:99px;overflow:hidden;margin-bottom:6px"><div id="mcd-modal-bar" style="height:100%;width:0%;background:#00e676"></div></div>' +
      '<div id="mcd-modal-nums" style="color:#8b949e;font-size:12px;margin-bottom:12px">۰ / ۰</div>' +
      '<div style="display:flex;gap:8px;flex-wrap:wrap">' +
      '<button type="button" id="mcd-modal-start" style="flex:1;background:#238636;color:#fff;border:0;border-radius:10px;padding:9px 12px;cursor:pointer">شروع دانلود</button>' +
      '<button type="button" id="mcd-modal-pause" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:10px;padding:9px 12px;cursor:pointer">توقف</button>' +
      '<button type="button" id="mcd-modal-retry" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:10px;padding:9px 12px;cursor:pointer">تلاش مجدد</button></div></div>';
    document.body.appendChild(modal);
    document.getElementById("mcd-modal-x").onclick = function () { modal.style.display = "none"; };
    document.getElementById("mcd-modal-start").onclick = function () {
      state.consented = true; lsSet(CONSENT_KEY, "yes"); startDownload(false);
    };
    document.getElementById("mcd-modal-pause").onclick = function () {
      state.stopFlag = true; state.running = false; renderProgress("متوقف شد");
    };
    document.getElementById("mcd-modal-retry").onclick = function () { startDownload(true); };
    return modal;
  }
  function openModal() { ensureModal(); modal.style.display = "flex"; renderProgress(); }

  function renderProgress(statusText) {
    ensureModal();
    var pct = state.total ? Math.floor((state.cached / state.total) * 100) : 0;
    var bar = document.getElementById("mcd-modal-bar");
    var nums = document.getElementById("mcd-modal-nums");
    var st = document.getElementById("mcd-modal-status");
    if (bar) bar.style.width = pct + "%";
    if (nums) nums.textContent = "تأییدشده: " + state.cached + " / " + state.total + " (" + pct + "٪)";
    if (st) {
      if (statusText) st.textContent = statusText;
      else if (state.cached === state.total && state.total > 0 && state.failed === 0) st.textContent = "دانلود شد";
      else if (state.running) st.textContent = "در حال دانلود…";
      else st.textContent = "آماده";
    }
  }

  function markPackReady() {
    state.packReady = true; lsSet(DONE_KEY, "1"); state.autoSync = true; state.userOverride = false;
    state.enabled = !state.online; lsSet(ENABLED_KEY, state.enabled ? "1" : "0"); updateLeverUI();
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
    return fetch(url, { credentials: "same-origin", cache: "no-cache" })
      .then(function (res) {
        if (!res || !res.ok || res.type === "opaque") throw { code: "http", message: "bad" };
        return res.blob().then(function (blob) {
          var putRes = new Response(blob, { status: res.status, statusText: res.statusText, headers: res.headers });
          return caches.open(CACHE_NAME).then(function (cache) {
            return cache.put(url, putRes).then(function () {
              return cache.match(url).then(function (m) {
                if (!m) throw { code: "verify", message: "fail" };
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
      for (var i = 0; i < STATIC_ASSETS.length; i++) add(STATIC_ASSETS[i]);
      for (var j = 0; j < locs.length; j++) { var p = pathFromLoc(locs[j]); if (p) add(p); }
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
    for (var i = 0; i < list.length; i++) state.byPath[list[i].path] = list[i];
    return idbGetAll("files").then(function (rows) {
      for (var j = 0; j < (rows || []).length; j++) {
        var row = rows[j], item = state.byPath[row.path];
        if (item) {
          item.status = row.status || "pending";
          if (item.status === "downloading" || item.status === "retrying") item.status = "pending";
        }
      }
      recount();
      if (state.cached === state.total && state.total > 0 && state.failed === 0) markPackReady();
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
    if (state.running || !navigator.onLine) return;
    state.consented = true; lsSet(CONSENT_KEY, "yes");
    state.stopFlag = false; state.running = true; renderProgress("در حال دانلود…");
    var profile = profileNetwork();
    if (!profile.concurrency) { state.running = false; return; }
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
        if (state.cached === state.total && state.failed === 0) { renderProgress("دانلود شد"); markPackReady(); }
        else if (state.failed > 0) renderProgress("دانلود ناقص");
      }
    }
    pump();
  }

  function preparePack(openUi) {
    return loadManifest().then(function (manifest) {
      return hydrate(manifest).then(function () {
        if (openUi) openModal();
        if (state.consented && state.cached < state.total && navigator.onLine) {
          setTimeout(function () { if (!state.running) startDownload(false); }, 300);
        }
      });
    });
  }

  function onUserEnableOffline() {
    state.enabled = true; lsSet(ENABLED_KEY, "1"); lsSet(CONSENT_KEY, "yes"); state.consented = true; updateLeverUI();
  }
  function onUserDisableOffline() {
    state.enabled = false; lsSet(ENABLED_KEY, "0"); state.stopFlag = true; state.running = false; updateLeverUI();
  }

  function registerSW() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    return navigator.serviceWorker.register((SCOPE_BASE + "sw.js").replace(/([^:]\/)\/+/g, "$1"), { scope: SCOPE_BASE }).catch(function () { return null; });
  }

  function bindConnectivity() {
    window.addEventListener("online", function () {
      state.online = true;
      if (state.packReady) { state.userOverride = false; state.enabled = false; lsSet(ENABLED_KEY, "0"); }
      updateLeverUI();
    });
    window.addEventListener("offline", function () {
      state.online = false;
      if (state.packReady) { state.userOverride = false; state.enabled = true; lsSet(ENABLED_KEY, "1"); }
      updateLeverUI();
    });
  }

  function init() {
    ensureToggleMounted();
    bindConnectivity();
    registerSW().then(function () {
      state.consented = lsGet(CONSENT_KEY) === "yes";
      state.packReady = lsGet(DONE_KEY) === "1";
      if (state.packReady) { state.enabled = !navigator.onLine; state.autoSync = true; }
      updateLeverUI();
      if (state.consented && navigator.onLine) preparePack(false);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
