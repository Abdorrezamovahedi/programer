/**
 * MCD Code Up — seamless offline for the whole site
 *
 * On enter: download every page + assets into browser cache
 * While offline: site keeps working (Service Worker serves cache)
 * When all tabs closed: cache is removed to free storage
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  var SESSION_KEY = "mcd_full_offline_session_v3";
  var FULL_DONE_KEY = "mcd_full_prefetch_done_v3";

  var SCOPE_BASE = (function () {
    var p = location.pathname || "/";
    if (p.indexOf("/programer") === 0) return "/programer/";
    return "/";
  })();

  function sessionActive() {
    try {
      return sessionStorage.getItem(SESSION_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function markSession() {
    try {
      sessionStorage.setItem(SESSION_KEY, "1");
    } catch (e) {}
  }

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

  function postToSW(msg) {
    return new Promise(function (resolve) {
      if (!navigator.serviceWorker) {
        resolve(null);
        return;
      }

      function send(controller) {
        if (!controller) {
          resolve(null);
          return;
        }
        var ch = new MessageChannel();
        var settled = false;
        function done(v) {
          if (settled) return;
          settled = true;
          resolve(v);
        }
        ch.port1.onmessage = function (ev) {
          done(ev.data);
        };
        try {
          controller.postMessage(msg, [ch.port2]);
        } catch (e) {
          done(null);
        }
        setTimeout(function () {
          done(null);
        }, 180000);
      }

      if (navigator.serviceWorker.controller) {
        send(navigator.serviceWorker.controller);
      } else {
        navigator.serviceWorker.ready
          .then(function (reg) {
            send((reg && reg.active) || navigator.serviceWorker.controller);
          })
          .catch(function () {
            resolve(null);
          });
      }
    });
  }

  function notifySW(type) {
    try {
      if (navigator.serviceWorker && navigator.serviceWorker.controller) {
        navigator.serviceWorker.controller.postMessage({ type: type });
      }
    } catch (e) {}
  }

  function clearOfflineCaches() {
    var tasks = [];
    if (window.caches && caches.keys) {
      tasks.push(
        caches
          .keys()
          .then(function (keys) {
            return Promise.all(
              keys.map(function (k) {
                if (k.indexOf("mcd-offline") === 0) return caches.delete(k);
              })
            );
          })
          .catch(function () {})
      );
    }
    tasks.push(postToSW({ type: "CLEAR_CACHE" }));
    return Promise.all(tasks);
  }

  function registerSW() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    var swUrl = (SCOPE_BASE + "sw.js").replace(/([^:]\/)\//g, "$1");
    return navigator.serviceWorker
      .register(swUrl, { scope: SCOPE_BASE })
      .then(function () {
        return navigator.serviceWorker.ready;
      })
      .catch(function (err) {
        console.warn("[MCD offline] SW register failed", err);
        return null;
      });
  }

  function absoluteUrl(path) {
    try {
      return new URL(path, location.origin + SCOPE_BASE).href;
    } catch (e) {
      return path;
    }
  }

  function loadSitemapUrls() {
    return fetch(absoluteUrl("sitemap.xml"), { credentials: "same-origin" })
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
      .catch(function () {
        return [];
      });
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
          "position:fixed",
          "bottom:18px",
          "left:50%",
          "transform:translateX(-50%)",
          "z-index:100000",
          "max-width:92vw",
          "padding:10px 16px",
          "border-radius:10px",
          "background:#0d1117",
          "color:#e6edf3",
          "border:1px solid #30363d",
          "font:13px/1.5 sans-serif",
          "box-shadow:0 8px 24px rgba(0,0,0,.35)",
          "opacity:0",
          "transition:opacity .25s",
          "pointer-events:none",
          "text-align:center"
        ].join(";");
        (document.body || document.documentElement).appendChild(el);
      }
      el.style.borderColor = ok ? "#00e676" : "#30363d";
      el.textContent = text;
      el.style.opacity = "1";
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(function () {
        el.style.opacity = "0";
      }, 4500);
    } catch (e) {}
  }

  function prefetchEntireSite() {
    if (fullPrefetchDone()) return Promise.resolve();

    showToast("در حال آماده‌سازی کل سایت برای حالت آفلاین…");

    return loadSitemapUrls().then(function (urls) {
      if (!urls.length) {
        urls = [
          absoluteUrl(""),
          absoluteUrl("index.html"),
          absoluteUrl("python/"),
          absoluteUrl("html/"),
          absoluteUrl("css/"),
          absoluteUrl("javascript/"),
          absoluteUrl("php/"),
          absoluteUrl("tamrin/")
        ];
      }

      var extras = [
        absoluteUrl("assets/css/main.css"),
        absoluteUrl("assets/js/boot-loader.js"),
        absoluteUrl("assets/js/app.js"),
        absoluteUrl("assets/js/home.js"),
        absoluteUrl("assets/js/mcd-motion.js"),
        absoluteUrl("assets/js/offline-session.js"),
        absoluteUrl("assets/js/search.js"),
        absoluteUrl("assets/js/exercises.js"),
        absoluteUrl("assets/js/tamrin-filter.js"),
        absoluteUrl("assets/img/favicon.svg"),
        absoluteUrl("assets/img/og-default.svg"),
        absoluteUrl("404.html")
      ];
      for (var i = 0; i < extras.length; i++) {
        if (urls.indexOf(extras[i]) === -1) urls.push(extras[i]);
      }

      return postToSW({ type: "CACHE_URLS", urls: urls }).then(function (res) {
        markFullPrefetchDone();
        showToast("سایت آماده است — حتی بدون اینترنت کامل کار می‌کند", true);
        return res;
      });
    });
  }

  function bindLeaveHandlers() {
    notifySW("PAGE_SHOW");

    /* Only signal leave when the page is really unloading — not on app switch alone */
    window.addEventListener(
      "pagehide",
      function (ev) {
        /* persisted = back-forward cache; still treat as possible leave */
        notifySW("PAGE_HIDE");
      },
      { capture: true }
    );

    window.addEventListener(
      "pageshow",
      function () {
        notifySW("PAGE_SHOW");
      },
      { capture: true }
    );

    window.addEventListener("online", function () {
      showToast("اتصال اینترنت برقرار شد", true);
    });
    window.addEventListener("offline", function () {
      showToast("بدون اینترنت — سایت از حافظه دستگاه اجرا می‌شود", true);
    });
  }

  function init() {
    var boot = Promise.resolve();

    if (!sessionActive()) {
      boot = clearOfflineCaches().then(function () {
        markSession();
      });
    } else {
      markSession();
    }

    boot
      .then(function () {
        return registerSW();
      })
      .then(function () {
        bindLeaveHandlers();
        setTimeout(function () {
          prefetchEntireSite();
        }, 500);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
