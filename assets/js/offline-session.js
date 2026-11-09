/**
 * MCD offline — background only, never slow the live site
 * - Site stays online and fast for the user
 * - After a delay, quietly caches pages with LOW concurrency on mobile
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  var CACHE_NAME = "mcd-offline-v3";
  var SESSION_KEY = "mcd_full_offline_session_v3";
  var FULL_DONE_KEY = "mcd_full_prefetch_done_v3";

  var isMobile = false;
  try {
    isMobile =
      window.matchMedia("(max-width:900px)").matches ||
      navigator.maxTouchPoints > 1 ||
      /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent || "");
  } catch (e) {}

  var SCOPE_BASE = (function () {
    var p = location.pathname || "/";
    if (p.indexOf("/programer") === 0) return "/programer/";
    return "/";
  })();

  function fullPrefetchDone() {
    try {
      return sessionStorage.getItem(FULL_DONE_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function markFullPrefetchDone() {
    try {
      sessionStorage.setItem(FULL_DONE_KEY, "1");
    } catch (e) {}
  }

  function absoluteUrl(path) {
    try {
      return new URL(path, location.origin + SCOPE_BASE).href;
    } catch (e) {
      return path;
    }
  }

  function notifySW(type) {
    try {
      if (navigator.serviceWorker && navigator.serviceWorker.controller) {
        navigator.serviceWorker.controller.postMessage({ type: type });
      }
    } catch (e) {}
  }

  function registerSW() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    var swUrl = (SCOPE_BASE + "sw.js").replace(/([^:]\/)\//g, "$1");
    return navigator.serviceWorker.register(swUrl, { scope: SCOPE_BASE }).catch(function () {
      return null;
    });
  }

  function loadSitemapUrls() {
    return fetch(absoluteUrl("sitemap.xml"), {
      credentials: "same-origin",
      cache: "force-cache",
      priority: "low"
    })
      .then(function (r) {
        if (!r.ok) throw new Error("sitemap");
        return r.text();
      })
      .then(function (xml) {
        var urls = [];
        var seen = {};
        var re = /<loc>\s*([^<]+)\s*<\/loc>/gi;
        var m;
        while ((m = re.exec(xml))) {
          var u = m[1].trim();
          if (u && !seen[u]) {
            seen[u] = 1;
            urls.push(u);
          }
        }
        return urls;
      });
  }

  function coreAssetUrls() {
    return [
      absoluteUrl(""),
      absoluteUrl("index.html"),
      absoluteUrl("404.html"),
      absoluteUrl("assets/css/main.css"),
      absoluteUrl("assets/js/boot-loader.js"),
      absoluteUrl("assets/js/app.js"),
      absoluteUrl("assets/js/home.js"),
      absoluteUrl("assets/js/mcd-motion.js"),
      absoluteUrl("assets/js/offline-session.js"),
      absoluteUrl("assets/js/search.js"),
      absoluteUrl("assets/img/favicon.svg"),
      absoluteUrl("python/"),
      absoluteUrl("html/"),
      absoluteUrl("css/"),
      absoluteUrl("javascript/"),
      absoluteUrl("php/"),
      absoluteUrl("tamrin/")
    ];
  }

  var toastEl = null;
  function showMini(msg) {
    try {
      if (!toastEl) {
        toastEl = document.createElement("div");
        toastEl.style.cssText =
          "position:fixed;bottom:10px;left:50%;transform:translateX(-50%);z-index:99990;max-width:90vw;padding:6px 10px;border-radius:8px;background:rgba(13,17,23,.85);color:#8b949e;border:1px solid #30363d;font:11px/1.4 sans-serif;direction:rtl;pointer-events:none";
        document.body.appendChild(toastEl);
      }
      toastEl.textContent = msg;
      toastEl.style.opacity = "1";
    } catch (e) {}
  }

  function hideMini(finalMsg) {
    try {
      if (!toastEl) return;
      if (finalMsg) toastEl.textContent = finalMsg;
      setTimeout(function () {
        if (!toastEl) return;
        toastEl.style.opacity = "0";
        setTimeout(function () {
          if (toastEl && toastEl.parentNode) toastEl.parentNode.removeChild(toastEl);
          toastEl = null;
        }, 400);
      }, 2500);
    } catch (e) {}
  }

  function lowFetch(url) {
    try {
      return fetch(url, { credentials: "same-origin", cache: "force-cache", priority: "low" });
    } catch (e) {
      return fetch(url, { credentials: "same-origin" });
    }
  }

  function cacheAllUrls(urls) {
    if (!window.caches) return Promise.resolve({ total: 0, ok: 0, fail: 0 });

    var total = urls.length;
    var done = 0;
    var ok = 0;
    var concurrency = isMobile ? 3 : 8;
    var index = 0;
    var lastUi = 0;

    return caches.open(CACHE_NAME).then(function (cache) {
      function putOne(url) {
        return lowFetch(url)
          .then(function (res) {
            if (!res || !res.ok) throw new Error("bad");
            return cache.put(url, res);
          })
          .then(function () {
            ok += 1;
            done += 1;
            var now = Date.now();
            if (now - lastUi > 800 || done === total) {
              lastUi = now;
              showMini("ذخیره پس‌زمینه " + done + "/" + total);
            }
          })
          .catch(function () {
            done += 1;
          });
      }

      function worker() {
        if (index >= urls.length) return Promise.resolve();
        var url = urls[index++];
        return putOne(url).then(worker);
      }

      var workers = [];
      for (var w = 0; w < concurrency; w++) workers.push(worker());
      return Promise.all(workers).then(function () {
        return { total: total, ok: ok, fail: total - ok };
      });
    });
  }

  function uniqueUrls(list) {
    var seen = {};
    var out = [];
    for (var i = 0; i < list.length; i++) {
      var u = list[i];
      if (u && !seen[u]) {
        seen[u] = 1;
        out.push(u);
      }
    }
    return out;
  }

  function prefetchEntireSite() {
    if (fullPrefetchDone()) return;
    if (!navigator.onLine) return;

    loadSitemapUrls()
      .catch(function () {
        return [];
      })
      .then(function (sitemapUrls) {
        var all = uniqueUrls(coreAssetUrls().concat(sitemapUrls));
        showMini("شروع ذخیره پس‌زمینه " + all.length + " صفحه…");
        return cacheAllUrls(all).then(function (stats) {
          markFullPrefetchDone();
          hideMini("ذخیره شد: " + stats.ok + " صفحه");
        });
      })
      .catch(function () {});
  }

  function init() {
    registerSW().then(function () {
      notifySW("PAGE_SHOW");
      window.addEventListener(
        "pagehide",
        function () {
          notifySW("PAGE_HIDE");
        },
        { capture: true }
      );

      /* Start caching only when browser is idle-ish */
      var start = function () {
        prefetchEntireSite();
      };
      if (typeof requestIdleCallback === "function") {
        requestIdleCallback(start, { timeout: 4000 });
      } else {
        setTimeout(start, 2000);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
