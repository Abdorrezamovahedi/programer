/**
 * MCD offline — header toggle + download modal + auto online/offline + version sync
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  var CACHE_NAME = "mcd-offline-v5";
  var DB_NAME = "mcd_offline_db_v5";
  var DB_VER = 1;
  var MANIFEST_VERSION = "2026-11-10-v1";
  var MAX_ATTEMPTS = 3;
  var CONSENT_KEY = "mcd_offline_consent_v1";
  var ENABLED_KEY = "mcd_offline_enabled_v1";

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
    consented: false, enabled: false, online: navigator.onLine !== false
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
        if (typeof c.downlink === "number") {
          if (c.downlink > 0 && c.downlink < 0.5) level = "very-slow";
          else if (c.downlink < 1.5 && level === "fast") level = "slow";
          else if (c.downlink >= 8) level = "fast";
        }
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

  function injectHeaderToggle() {
    var nav = document.querySelector("header nav");
    if (!nav || document.getElementById("mcd-offline-nav")) return;
    var wrap = document.createElement("label");
    wrap.id = "mcd-offline-nav";
    wrap.setAttribute("title", "فعال‌سازی ذخیره آفلاین سایت");
    wrap.style.cssText = "display:inline-flex;align-items:center;gap:6px;cursor:pointer;margin-right:4px;padding:4px 8px;border-radius:8px;border:1px solid #238636;color:#00e676;font-size:12px;user-select:none;white-space:nowrap";
    var cb = document.createElement("input");
    cb.type = "checkbox";
    cb.id = "mcd-offline-check";
    cb.style.cssText = "accent-color:#00e676;width:14px;height:14px;cursor:pointer";
    var text = document.createElement("span");
    text.textContent = "آفلاین";
    var badge = document.createElement("span");
    badge.id = "mcd-net-badge";
    badge.style.cssText = "font-size:10px;padding:1px 6px;border-radius:99px;border:1px solid #30363d;color:#8b949e";
    wrap.appendChild(cb); wrap.appendChild(text); wrap.appendChild(badge);
    nav.appendChild(wrap);
    cb.checked = state.enabled || state.consented;
    updateNetBadge();
    cb.addEventListener("change", function () {
      if (cb.checked) onUserEnableOffline(); else onUserDisableOffline();
    });
  }

  function updateNetBadge() {
    var badge = document.getElementById("mcd-net-badge");
    var cb = document.getElementById("mcd-offline-check");
    if (!badge) return;
    if (state.online) {
      badge.textContent = "آنلاین"; badge.style.color = "#00e676"; badge.style.borderColor = "#238636";
    } else {
      badge.textContent = "آفلاین"; badge.style.color = "#f0b429"; badge.style.borderColor = "#f0b429";
      if (cb && state.consented) cb.checked = true;
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
      '<div style="width:min(440px,100%);background:#0d1117;border:1px solid #238636;border-radius:16px;padding:18px 16px;color:#e6edf3;box-shadow:0 16px 48px rgba(0,0,0,.5)">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">' +
      '<b style="color:#00e676;font-size:17px">ذخیره آفلاین سایت</b>' +
      '<button type="button" id="mcd-modal-x" style="background:transparent;border:0;color:#8b949e;font-size:18px;cursor:pointer">×</button></div>' +
      '<p style="margin:0 0 10px;line-height:1.7;color:#c9d1d9;font-size:13px">با فعال‌سازی، درس‌ها روی همین دستگاه و همین مرورگر ذخیره می‌شوند تا <b style="color:#00e676">بدون اینترنت</b> هم بتوانید مطالعه کنید.</p>' +
      '<ul style="margin:0 0 12px;padding:0 18px 0 0;line-height:1.75;color:#8b949e;font-size:12px">' +
      '<li>در تب مرورگر و وب‌اپ (نصب‌شده) روی همین دستگاه مشترک است</li>' +
      '<li>وقتی دانلود تمام شد پیام «دانلود شد» می‌آید</li>' +
      '<li>اگر نسخه سایت عوض شود، در حالت آنلاین همگام می‌شود</li></ul>' +
      '<div id="mcd-modal-status" style="color:#8b949e;font-size:12px;margin-bottom:6px">آماده</div>' +
      '<div style="height:8px;background:#21262d;border-radius:99px;overflow:hidden;margin-bottom:6px">' +
      '<div id="mcd-modal-bar" style="height:100%;width:0%;background:#00e676;transition:width .2s"></div></div>' +
      '<div id="mcd-modal-nums" style="color:#8b949e;font-size:12px;margin-bottom:12px">۰ / ۰</div>' +
      '<div style="display:flex;gap:8px;flex-wrap:wrap">' +
      '<button type="button" id="mcd-modal-start" style="flex:1;min-width:120px;background:#238636;color:#fff;border:0;border-radius:10px;padding:9px 12px;cursor:pointer;font-weight:600">شروع دانلود</button>' +
      '<button type="button" id="mcd-modal-pause" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:10px;padding:9px 12px;cursor:pointer">توقف</button>' +
      '<button type="button" id="mcd-modal-retry" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:10px;padding:9px 12px;cursor:pointer">تلاش مجدد</button></div></div>';
    document.body.appendChild(modal);
    document.getElementById("mcd-modal-x").onclick = function () { modal.style.display = "none"; };
    modal.addEventListener("click", function (e) { if (e.target === modal) modal.style.display = "none"; });
    document.getElementById("mcd-modal-start").onclick = function () { startDownload(false); };
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
    if (nums) nums.textContent = "تأییدشده: " + state.cached + " / " + state.total + " (" + pct + "٪) · ناموفق: " + state.failed + " · مانده: " + state.pending;
    if (st) {
      if (statusText) st.textContent = statusText;
      else if (state.cached === state.total && state.total > 0 && state.failed === 0) st.textContent = "دانلود شد";
      else if (state.failed > 0 && state.pending === 0 && !state.running) st.textContent = "دانلود ناقص — روی تلاش مجدد بزنید";
      else if (state.running) st.textContent = "در حال دانلود و تأیید فایل‌ها…";
      else st.textContent = "آماده برای شروع";
    }
  }

  function recount() {
    var c = 0, f = 0, p = 0, d = 0;
    for (var i = 0; i < state.resources.length; i++) {
      var s = state.resources[i].status;
      if (s === "cached") c++; else if (s === "failed") f++;
      else if (s === "downloading" || s === "retrying") d++; else p++;
    }
    state.cached = c; state.failed = f; state.pending = p; state.downloading = d;
  }

  function cacheOneVerified(path) {
    var url = absUrl(path);
    return fetch(url, { credentials: "same-origin", cache: "no-cache" })
      .then(function (res) {
        if (!res) throw { code: "network", message: "empty" };
        if (!res.ok) throw { code: "http", message: "HTTP " + res.status };
        if (res.type === "opaque") throw { code: "opaque", message: "opaque" };
        if (res.status === 206) throw { code: "partial", message: "partial" };
        return res.blob().then(function (blob) {
          var putRes = new Response(blob, { status: res.status, statusText: res.statusText, headers: res.headers });
          return caches.open(CACHE_NAME).then(function (cache) {
            return cache.put(url, putRes).then(function () {
              return cache.match(url).then(function (matched) {
                if (!matched) throw { code: "verify", message: "match failed" };
                return true;
              });
            });
          });
        });
      })
      .catch(function (err) {
        if (err && err.name === "QuotaExceededError") throw { code: "quota", message: "storage full" };
        if (err && err.code) throw err;
        throw { code: "network", message: String((err && err.message) || err || "fail") };
      });
  }

  function pathFromLoc(loc) {
    try {
      var u = new URL(loc);
      var path = u.pathname || "/";
      if (path.indexOf("/programer/") === 0) path = path.slice("/programer/".length);
      else if (path.indexOf("/programer") === 0) path = path.slice("/programer".length).replace(/^\//, "");
      if (!path || path === "/") return "index.html";
      return path.replace(/^\//, "");
    } catch (e) { return null; }
  }

  function loadManifest() {
    var metaP = fetch(absUrl("offline-manifest-meta.json"), { credentials: "same-origin", cache: "no-cache" })
      .then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; });
    var mapP = fetch(absUrl("sitemap.xml"), { credentials: "same-origin", cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error("sitemap"); return r.text(); })
      .then(function (xml) {
        var urls = [], re = /<loc>\s*([^<]+)\s*<\/loc>/gi, m;
        while ((m = re.exec(xml))) urls.push(m[1].trim());
        return urls;
      }).catch(function () { return []; });
    return Promise.all([metaP, mapP]).then(function (pair) {
      var meta = pair[0] || {}, locs = pair[1] || [];
      if (meta.version) MANIFEST_VERSION = meta.version;
      if (meta.cacheName) CACHE_NAME = meta.cacheName;
      var seen = {}, resources = [];
      function add(path) { if (!path || seen[path]) return; seen[path] = 1; resources.push({ p: path, t: classify(path) }); }
      for (var i = 0; i < STATIC_ASSETS.length; i++) add(STATIC_ASSETS[i]);
      for (var j = 0; j < locs.length; j++) { var p = pathFromLoc(locs[j]); if (p) add(p); }
      return { version: MANIFEST_VERSION, cacheName: CACHE_NAME, resources: resources };
    });
  }

  function hydrate(manifest, forceResync) {
    MANIFEST_VERSION = manifest.version || MANIFEST_VERSION;
    if (manifest.cacheName) CACHE_NAME = manifest.cacheName;
    var list = (manifest.resources || []).map(function (r) {
      return { path: r.p || r.path, type: r.t || r.type || "other", status: "pending", attempts: 0, error: null };
    });
    state.resources = list; state.total = list.length; state.byPath = {};
    for (var i = 0; i < list.length; i++) state.byPath[list[i].path] = list[i];
    return idbGetMeta("manifestVersion").then(function (prevVer) {
      var versionChanged = prevVer && prevVer !== MANIFEST_VERSION;
      return idbGetAll("files").then(function (rows) {
        if (!forceResync && !versionChanged && rows && rows.length) {
          for (var j = 0; j < rows.length; j++) {
            var row = rows[j], item = state.byPath[row.path];
            if (item) {
              item.status = row.status || "pending";
              item.attempts = row.attempts || 0;
              item.error = row.error || null;
              if (item.status === "downloading" || item.status === "retrying") item.status = "pending";
            }
          }
        } else if (versionChanged) {
          for (var k = 0; k < list.length; k++) { list[k].status = "pending"; list[k].attempts = 0; }
        }
        return idbSetMeta("manifestVersion", MANIFEST_VERSION).then(function () {
          recount();
          renderProgress(versionChanged ? "نسخه سایت تغییر کرده — در حال همگام‌سازی…" : null);
          return versionChanged;
        });
      });
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
    if (!state.consented && !state.enabled) return;
    if (state.running) return;
    if (!navigator.onLine) { renderProgress("اینترنت ندارید — فقط فایل‌های قبلی قابل استفاده‌اند"); return; }
    state.stopFlag = false; state.running = true; renderProgress("در حال دانلود و تأیید فایل‌ها…");
    var profile = profileNetwork();
    if (!profile.concurrency) { state.running = false; renderProgress("حالت صرفه‌جویی اینترنت فعال است"); return; }
    var active = 0, concurrency = profile.concurrency;
    function pump() {
      if (state.stopFlag) { state.running = false; renderProgress("متوقف شد"); return; }
      while (active < concurrency) {
        var item = pickNext(retryOnly);
        if (!item) break;
        active++;
        item.status = item.attempts > 0 ? "retrying" : "downloading";
        item.attempts += 1; persistItem(item); recount(); renderProgress();
        (function (current) {
          cacheOneVerified(current.path)
            .then(function () { current.status = "cached"; current.error = null; return persistItem(current); })
            .catch(function (err) {
              current.error = (err && err.code ? err.code + ": " : "") + ((err && err.message) || "error");
              current.status = "failed"; return persistItem(current);
            })
            .then(function () { active--; recount(); renderProgress(); setTimeout(pump, profile.pauseMs || 0); });
        })(item);
      }
      if (active === 0) {
        state.running = false; recount();
        if (state.cached === state.total && state.failed === 0) {
          renderProgress("دانلود شد");
          idbSetMeta("complete", true);
          lsSet("mcd_offline_done_v1", "1");
          try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch (ePersist) {}
        } else if (state.failed > 0) renderProgress("دانلود ناقص — " + state.failed + " فایل ناموفق");
        else renderProgress("آماده");
      }
    }
    pump();
  }

  function preparePack(openUi) {
    return loadManifest().then(function (manifest) {
      return hydrate(manifest, false).then(function (versionChanged) {
        if (openUi) openModal();
        recount();
        if (!versionChanged && state.cached === state.total && state.total > 0 && state.failed === 0) {
          renderProgress("دانلود شد");
          lsSet("mcd_offline_done_v1", "1");
          return;
        }
        if (versionChanged || state.cached < state.total) {
          setTimeout(function () { if (!state.running) startDownload(false); }, 400);
        }
      });
    }).catch(function (err) {
      console.warn("[MCD offline]", err);
      renderProgress("خطا در آماده‌سازی فهرست");
    });
  }

  function onUserEnableOffline() {
    state.enabled = true; lsSet(ENABLED_KEY, "1"); lsSet(CONSENT_KEY, "yes"); state.consented = true;
    openModal(); preparePack(false);
  }
  function onUserDisableOffline() {
    state.enabled = false; lsSet(ENABLED_KEY, "0"); state.stopFlag = true; state.running = false;
    if (state.online) { var cb = document.getElementById("mcd-offline-check"); if (cb) cb.checked = false; }
  }

  function registerSW() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    var swUrl = (SCOPE_BASE + "sw.js").replace(/([^:]\/)\/+/g, "$1");
    return navigator.serviceWorker.register(swUrl, { scope: SCOPE_BASE }).catch(function () { return null; });
  }

  function bindConnectivity() {
    function applyOnline() {
      state.online = true; updateNetBadge();
      if (state.consented) preparePack(false);
    }
    function applyOffline() {
      state.online = false; updateNetBadge();
      var cb = document.getElementById("mcd-offline-check");
      if (cb && state.consented) cb.checked = true;
    }
    window.addEventListener("online", applyOnline);
    window.addEventListener("offline", applyOffline);
    if (navigator.onLine) applyOnline(); else applyOffline();
  }

  function init() {
    injectHeaderToggle();
    bindConnectivity();
    try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch (e0) {}
    registerSW().then(function () {
      var consent = lsGet(CONSENT_KEY);
      var enabled = lsGet(ENABLED_KEY) === "1";
      state.consented = consent === "yes";
      state.enabled = enabled || state.consented;
      var cb = document.getElementById("mcd-offline-check");
      if (cb) cb.checked = state.enabled || !navigator.onLine;
      if (state.consented && navigator.onLine) preparePack(false);
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
