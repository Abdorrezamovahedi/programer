/**
 * MCD Code Up — Offline session cache
 *
 * - Registers Service Worker for offline use
 * - Caches pages as the user browses
 * - When user enters a language section, prefetches that language's pages
 * - On a NEW browser session (user left site and came back), clears offline cache
 *   so device storage does not grow indefinitely
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  var SESSION_KEY = "mcd_offline_session_v1";
  var PREFETCHED_KEY = "mcd_lang_prefetched_v1";
  var SCOPE_BASE = (function () {
    var p = location.pathname || "/";
    var idx = p.indexOf("/programer");
    if (idx === 0) return "/programer/";
    // local server or custom domain at root
    return "/";
  })();

  var LANGS = ["python", "html", "css", "javascript", "php", "tamrin"];

  function sessionActive() {
    try {
      return sessionStorage.getItem(SESSION_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function markSession() {
    try { sessionStorage.setItem(SESSION_KEY, "1"); } catch (e) {}
  }

  function getPrefetched() {
    try {
      return JSON.parse(sessionStorage.getItem(PREFETCHED_KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function setPrefetched(map) {
    try { sessionStorage.setItem(PREFETCHED_KEY, JSON.stringify(map)); } catch (e) {}
  }

  function postToSW(msg) {
    return new Promise(function (resolve) {
      if (!navigator.serviceWorker || !navigator.serviceWorker.controller) {
        resolve(null);
        return;
      }
      var ch = new MessageChannel();
      ch.port1.onmessage = function (ev) { resolve(ev.data); };
      try {
        navigator.serviceWorker.controller.postMessage(msg, [ch.port2]);
      } catch (e) {
        resolve(null);
      }
      setTimeout(function () { resolve(null); }, 8000);
    });
  }

  function clearOfflineCaches() {
    var tasks = [];
    if (window.caches && caches.keys) {
      tasks.push(
        caches.keys().then(function (keys) {
          return Promise.all(keys.map(function (k) {
            if (k.indexOf("mcd-offline") === 0) return caches.delete(k);
          }));
        }).catch(function () {})
      );
    }
    tasks.push(postToSW({ type: "CLEAR_CACHE" }));
    return Promise.all(tasks);
  }

  function registerSW() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    var swUrl = SCOPE_BASE.replace(/\/$/, "/") + "sw.js";
    // fix double slash
    swUrl = swUrl.replace(/([^:]\/)\//g, "$1");
    return navigator.serviceWorker.register(swUrl, { scope: SCOPE_BASE }).catch(function (err) {
      console.warn("[MCD offline] SW register failed", err);
      return null;
    });
  }

  function currentLanguage() {
    var path = (location.pathname || "").toLowerCase();
    for (var i = 0; i < LANGS.length; i++) {
      var lang = LANGS[i];
      if (path.indexOf("/" + lang + "/") !== -1 || path.endsWith("/" + lang) || path.indexOf("/" + lang + "/index") !== -1) {
        return lang;
      }
    }
    return null;
  }

  function absoluteUrl(path) {
    try {
      return new URL(path, location.origin + SCOPE_BASE).href;
    } catch (e) {
      return path;
    }
  }

  function loadSitemapUrls() {
    var sitemapUrl = absoluteUrl("sitemap.xml");
    return fetch(sitemapUrl, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("sitemap");
        return r.text();
      })
      .then(function (xml) {
        var urls = [];
        var re = /<loc>\s*([^<]+)\s*<\/loc>/gi;
        var m;
        while ((m = re.exec(xml))) {
          urls.push(m[1].trim());
        }
        return urls;
      })
      .catch(function () { return []; });
  }

  function filterLanguageUrls(allUrls, lang) {
    var needle = "/" + lang + "/";
    var out = [];
    for (var i = 0; i < allUrls.length; i++) {
      var u = allUrls[i];
      if (u.indexOf(needle) !== -1) out.push(u);
    }
    // also include language index
    var idx = absoluteUrl(lang + "/");
    if (out.indexOf(idx) === -1) out.unshift(idx);
    return out;
  }

  function prefetchLanguage(lang) {
    if (!lang) return Promise.resolve();
    var done = getPrefetched();
    if (done[lang]) return Promise.resolve();

    done[lang] = 1;
    setPrefetched(done);

    return loadSitemapUrls().then(function (all) {
      var urls = filterLanguageUrls(all, lang);
      if (!urls.length) {
        // fallback: at least cache current page & language index
        urls = [location.href, absoluteUrl(lang + "/"), absoluteUrl(lang + "/index.html")];
      }
      // Cap extreme sizes (php has many pages)
      if (urls.length > 350) urls = urls.slice(0, 350);

      showToast("در حال ذخیره‌سازی آفلاین بخش «" + lang + "»…");

      return postToSW({ type: "CACHE_URLS", urls: urls }).then(function () {
        showToast("بخش «" + lang + "» برای استفاده آفلاین آماده شد", true);
      });
    });
  }

  function cacheCurrentPage() {
    if (!window.caches) return;
    var req = location.href;
    caches.open("mcd-offline-v1").then(function (cache) {
      return fetch(req, { credentials: "same-origin" }).then(function (res) {
        if (res && res.ok) return cache.put(req, res);
      });
    }).catch(function () {});
  }

  var toastTimer = null;
  function showToast(text, ok) {
    try {
      var el = document.getElementById("mcd-offline-toast");
      if (!el) {
        el = document.createElement("div");
        el.id = "mcd-offline-toast";
        el.setAttribute("role", "status");
        el.style.cssText = [
          "position:fixed", "bottom:18px", "left:50%", "transform:translateX(-50%)",
          "z-index:100000", "max-width:92vw", "padding:10px 16px", "border-radius:10px",
          "background:#0d1117", "color:#e6edf3", "border:1px solid #30363d",
          "font:13px/1.5 sans-serif", "box-shadow:0 8px 24px rgba(0,0,0,.35)",
          "opacity:0", "transition:opacity .25s", "pointer-events:none", "text-align:center"
        ].join(";");
        (document.body || document.documentElement).appendChild(el);
      }
      el.style.borderColor = ok ? "#00e676" : "#30363d";
      el.textContent = text;
      el.style.opacity = "1";
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(function () { el.style.opacity = "0"; }, 3200);
    } catch (e) {}
  }

  function onOnline() {
    showToast("اتصال اینترنت برقرار شد", true);
  }
  function onOffline() {
    showToast("اینترنت قطع است — ادامه با نسخه ذخیره‌شده");
  }

  function init() {
    var boot = Promise.resolve();

    // New browser session? Clear previous offline cache to free storage.
    if (!sessionActive()) {
      boot = clearOfflineCaches().then(function () {
        markSession();
      });
    } else {
      markSession();
    }

    boot.then(function () {
      return registerSW();
    }).then(function () {
      cacheCurrentPage();

      var lang = currentLanguage();
      if (lang) {
        // slight delay so first paint isn't blocked
        setTimeout(function () { prefetchLanguage(lang); }, 1200);
      }

      window.addEventListener("online", onOnline);
      window.addEventListener("offline", onOffline);

      // Soft hint when user hides tab for a long time is NOT clearing —
      // clearing happens on next session start (sessionStorage gone).
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
