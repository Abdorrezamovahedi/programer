/**
 * MCD permanent offline pack — gentle background fill
 *
 * - First successful full download is remembered in localStorage (stays forever)
 * - Online: user uses live site; background fills missing pages slowly
 * - Offline: Service Worker serves the saved pack
 * - No aggressive mass-download that freezes mobile Chrome
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  var CACHE_NAME = "mcd-offline-v4";
  var DONE_KEY = "mcd_offline_pack_done_v4";
  var CURSOR_KEY = "mcd_offline_pack_cursor_v4";

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

  function absoluteUrl(path) {
    try {
      return new URL(path, location.origin + SCOPE_BASE).href;
    } catch (e) {
      return path;
    }
  }

  function isDone() {
    try {
      return localStorage.getItem(DONE_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function markDone() {
    try {
      localStorage.setItem(DONE_KEY, "1");
      localStorage.removeItem(CURSOR_KEY);
    } catch (e) {}
  }

  function getCursor() {
    try {
      return parseInt(localStorage.getItem(CURSOR_KEY) || "0", 10) || 0;
    } catch (e) {
      return 0;
    }
  }

  function setCursor(n) {
    try {
      localStorage.setItem(CURSOR_KEY, String(n));
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

  function coreUrls() {
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

  function unique(list) {
    var s = {};
    var o = [];
    for (var i = 0; i < list.length; i++) {
      if (list[i] && !s[list[i]]) {
        s[list[i]] = 1;
        o.push(list[i]);
      }
    }
    return o;
  }

  function lowFetch(url) {
    try {
      return fetch(url, { credentials: "same-origin", cache: "force-cache", priority: "low" });
    } catch (e) {
      return fetch(url, { credentials: "same-origin" });
    }
  }

  /**
   * Gentle fill: small batches + pause between batches
   * so Chrome on mobile stays usable.
   */
  function gentleFill(urls) {
    if (!window.caches || !navigator.onLine) return Promise.resolve();

    var batchSize = isMobile ? 4 : 10;
    var pauseMs = isMobile ? 700 : 250;
    var cursor = getCursor();
    if (cursor >= urls.length) {
      markDone();
      return Promise.resolve();
    }

    return caches.open(CACHE_NAME).then(function (cache) {
      function runBatch() {
        if (!navigator.onLine) return Promise.resolve();
        if (cursor >= urls.length) {
          markDone();
          return Promise.resolve();
        }

        var end = Math.min(cursor + batchSize, urls.length);
        var slice = urls.slice(cursor, end);

        return Promise.all(
          slice.map(function (url) {
            return lowFetch(url)
              .then(function (res) {
                if (res && res.ok) return cache.put(url, res);
              })
              .catch(function () {});
          })
        ).then(function () {
          cursor = end;
          setCursor(cursor);
          if (cursor >= urls.length) {
            markDone();
            return;
          }
          return new Promise(function (resolve) {
            setTimeout(function () {
              runBatch().then(resolve);
            }, pauseMs);
          });
        });
      }

      return runBatch();
    });
  }

  function startBackgroundPack() {
    if (isDone()) return;
    if (!navigator.onLine) return;

    loadSitemapUrls()
      .catch(function () {
        return [];
      })
      .then(function (map) {
        var all = unique(coreUrls().concat(map));
        return gentleFill(all);
      })
      .catch(function () {});
  }

  function init() {
    registerSW().then(function () {
      /* wait until page is calm */
      var delay = isMobile ? 8000 : 5000;
      setTimeout(function () {
        if (typeof requestIdleCallback === "function") {
          requestIdleCallback(
            function () {
              startBackgroundPack();
            },
            { timeout: 5000 }
          );
        } else {
          startBackgroundPack();
        }
      }, delay);
    });
  }

  if (document.readyState === "complete") init();
  else window.addEventListener("load", init);
})();
