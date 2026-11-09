/**
 * MCD Code Up — آنلاین کامل + ذخیره پس‌زمینه خیلی سریع
 *
 * وقتی اینترنت هست:
 *   - کاربر سایت را عادی و آنلاین می‌بیند (بدون تأخیر)
 *   - همزمان در پس‌زمینه همه ۱۷۰۰+ صفحه با اولویت پایین ذخیره می‌شوند
 * وقتی اینترنت قطع شد:
 *   - همان صفحات ذخیره‌شده از دستگاه سرو می‌شوند
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  var CACHE_NAME = "mcd-offline-v3";
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

  function absoluteUrl(path) {
    try {
      return new URL(path, location.origin + SCOPE_BASE).href;
    } catch (e) {
      return path;
    }
  }

  function notifySW(type, extra) {
    try {
      if (navigator.serviceWorker && navigator.serviceWorker.controller) {
        var msg = { type: type };
        if (extra) for (var k in extra) msg[k] = extra[k];
        navigator.serviceWorker.controller.postMessage(msg);
      }
    } catch (e) {}
  }

  function clearOfflineCaches() {
    if (!window.caches) return Promise.resolve();
    return caches.keys().then(function (keys) {
      return Promise.all(
        keys.map(function (k) {
          if (k.indexOf("mcd-offline") === 0) return caches.delete(k);
        })
      );
    }).catch(function () {});
  }

  function registerSW() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    var swUrl = (SCOPE_BASE + "sw.js").replace(/([^:]\/)\//g, "$1");
    return navigator.serviceWorker
      .register(swUrl, { scope: SCOPE_BASE })
      .then(function () {
        return navigator.serviceWorker.ready;
      })
      .catch(function () {
        return null;
      });
  }

  function loadSitemapUrls() {
    return fetch(absoluteUrl("sitemap.xml"), {
      credentials: "same-origin",
      cache: "no-cache",
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
      absoluteUrl("assets/js/exercises.js"),
      absoluteUrl("assets/js/tamrin-filter.js"),
      absoluteUrl("assets/img/favicon.svg"),
      absoluteUrl("assets/img/og-default.svg"),
      absoluteUrl("sitemap.xml"),
      absoluteUrl("python/"),
      absoluteUrl("html/"),
      absoluteUrl("css/"),
      absoluteUrl("javascript/"),
      absoluteUrl("php/"),
      absoluteUrl("tamrin/")
    ];
  }

  function ensureBar() {
    var el = document.getElementById("mcd-offline-progress");
    if (el) return el;
    el = document.createElement("div");
    el.id = "mcd-offline-progress";
    el.setAttribute("role", "status");
    el.style.cssText = [
      "position:fixed",
      "bottom:12px",
      "left:50%",
      "transform:translateX(-50%)",
      "z-index:99990",
      "width:min(360px,90vw)",
      "padding:8px 12px",
      "border-radius:10px",
      "background:rgba(13,17,23,.92)",
      "color:#8b949e",
      "border:1px solid #30363d",
      "font:12px/1.4 sans-serif",
      "text-align:center",
      "direction:rtl",
      "pointer-events:none",
      "opacity:.92"
    ].join(";");
    el.innerHTML =
      '<div id="mcd-off-text">آماده‌سازی پس‌زمینه…</div>' +
      '<div style="margin-top:6px;height:4px;background:#21262d;border-radius:99px;overflow:hidden">' +
      '<div id="mcd-off-bar" style="height:100%;width:0%;background:#00e676;transition:width .15s"></div></div>';
    (document.body || document.documentElement).appendChild(el);
    return el;
  }

  function setProgress(done, total) {
    try {
      var wrap = ensureBar();
      var text = document.getElementById("mcd-off-text");
      var bar = document.getElementById("mcd-off-bar");
      var pct = total ? Math.min(100, Math.round((done / total) * 100)) : 0;
      if (text)
        text.textContent =
          "ذخیره پس‌زمینه (سایت آنلاین است) — " + done + "/" + total + " — " + pct + "٪";
      if (bar) bar.style.width = pct + "%";
    } catch (e) {}
  }

  function hideProgress(msg, ok) {
    try {
      var wrap = ensureBar();
      var text = document.getElementById("mcd-off-text");
      var bar = document.getElementById("mcd-off-bar");
      if (text) {
        text.textContent = msg;
        text.style.color = ok ? "#00e676" : "#f85149";
      }
      if (bar) {
        bar.style.width = "100%";
        bar.style.background = ok ? "#00e676" : "#f85149";
      }
      setTimeout(function () {
        wrap.style.opacity = "0";
        wrap.style.transition = "opacity .35s";
        setTimeout(function () {
          if (wrap.parentNode) wrap.parentNode.removeChild(wrap);
        }, 400);
      }, 2800);
    } catch (e) {}
  }

  /** fetch با اولویت پایین تا مرور کاربر آنلاین گیر نکند */
  function lowFetch(url) {
    var opts = { credentials: "same-origin", cache: "no-cache", priority: "low" };
    try {
      return fetch(url, opts);
    } catch (e) {
      return fetch(url, { credentials: "same-origin", cache: "no-cache" });
    }
  }

  /**
   * ذخیره سریع موازی — روی UI اثر نمی‌گذارد
   * concurrency بالا = سرعت بیشتر
   */
  function cacheAllUrls(urls) {
    if (!window.caches) return Promise.reject(new Error("no cache"));

    var total = urls.length;
    var done = 0;
    var failed = [];
    var concurrency = 20;
    var index = 0;
    var lastUi = 0;

    return caches.open(CACHE_NAME).then(function (cache) {
      function putOne(url) {
        return lowFetch(url)
          .then(function (res) {
            if (!res || !res.ok) throw new Error("bad");
            return cache.put(url, res).then(function () {
              try {
                var u = new URL(url);
                if (u.pathname.endsWith("/index.html")) {
                  var dir = u.origin + u.pathname.replace(/\/index\.html$/, "/");
                  return cache.match(url).then(function (hit) {
                    if (hit) return cache.put(dir, hit.clone());
                  });
                }
              } catch (e) {}
            });
          })
          .then(function () {
            done += 1;
            var now = Date.now();
            if (now - lastUi > 200 || done === total) {
              lastUi = now;
              setProgress(done, total);
            }
          })
          .catch(function () {
            failed.push(url);
            done += 1;
            var now = Date.now();
            if (now - lastUi > 200 || done === total) {
              lastUi = now;
              setProgress(done, total);
            }
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
        if (!failed.length) return { total: total, ok: total, fail: 0 };

        var retryList = failed.slice();
        failed = [];
        done = 0;
        total = retryList.length;
        index = 0;
        lastUi = 0;

        function putRetry(url) {
          return lowFetch(url)
            .then(function (res) {
              if (!res || !res.ok) throw new Error("bad");
              return cache.put(url, res);
            })
            .then(function () {
              done += 1;
              setProgress(done, total);
            })
            .catch(function () {
              failed.push(url);
              done += 1;
              setProgress(done, total);
            });
        }

        function worker2() {
          if (index >= retryList.length) return Promise.resolve();
          var url = retryList[index++];
          return putRetry(url).then(worker2);
        }

        var workers2 = [];
        for (var w2 = 0; w2 < 12; w2++) workers2.push(worker2());
        return Promise.all(workers2).then(function () {
          return {
            total: urls.length,
            ok: urls.length - failed.length,
            fail: failed.length
          };
        });
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
    if (fullPrefetchDone()) return Promise.resolve();
    if (!navigator.onLine) return Promise.resolve();

    /* کاملاً غیرمسدودکننده — کاربر همزمان آنلاین کار می‌کند */
    return loadSitemapUrls()
      .catch(function () {
        return [];
      })
      .then(function (sitemapUrls) {
        var all = uniqueUrls(coreAssetUrls().concat(sitemapUrls));
        setProgress(0, all.length);
        return cacheAllUrls(all).then(function (stats) {
          markFullPrefetchDone();
          notifySW("CACHE_READY", { total: stats.total, ok: stats.ok });
          if (stats.fail === 0) {
            hideProgress("آماده‌سازی کامل شد — " + stats.ok + " صفحه ذخیره شد", true);
          } else {
            hideProgress(
              "آماده‌سازی انجام شد — " + stats.ok + " صفحه (" + stats.fail + " رد شد)",
              true
            );
          }
        });
      })
      .catch(function (err) {
        console.warn("[MCD offline]", err);
      });
  }

  function bindLeaveHandlers() {
    notifySW("PAGE_SHOW");
    window.addEventListener(
      "pagehide",
      function () {
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
  }

  function init() {
    /* ثبت SW و شروع پس‌زمینه — بدون بلوکه کردن صفحه */
    markSession();

    registerSW().then(function () {
      bindLeaveHandlers();

      /* اگر نشست جدید است، کش قدیمی را در پس‌زمینه پاک کن؛ صفحه را معطل نکن */
      if (!sessionActive()) {
        /* session flag already set above for this visit after clear path */
      }

      /* شروع فوری ذخیره پس‌زمینه — موازی با استفاده آنلاین کاربر */
      if (typeof requestIdleCallback === "function") {
        requestIdleCallback(
          function () {
            prefetchEntireSite();
          },
          { timeout: 800 }
        );
      } else {
        setTimeout(function () {
          prefetchEntireSite();
        }, 300);
      }
    });

    /* پاک‌سازی نشست قبلی بدون مسدود کردن UI */
    try {
      if (!sessionStorage.getItem(SESSION_KEY + "_booted")) {
        sessionStorage.setItem(SESSION_KEY + "_booted", "1");
        /* first page of this browser session */
        if (!sessionStorage.getItem(SESSION_KEY + "_cleared")) {
          sessionStorage.setItem(SESSION_KEY + "_cleared", "1");
          clearOfflineCaches().then(function () {
            /* allow fresh full download */
            try {
              sessionStorage.removeItem(FULL_DONE_KEY);
            } catch (e) {}
            prefetchEntireSite();
          });
          return;
        }
      }
    } catch (e) {}
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
