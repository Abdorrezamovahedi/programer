/**
 * MCD Code Up — ذخیره کامل کل سایت (۱۷۰۰+ صفحه) روی دستگاه کاربر
 *
 * - با ورود: همه URLهای sitemap + فایل‌های ضروری در Cache Storage ذخیره می‌شوند
 * - آفلاین: Service Worker همان فایل‌ها را مثل حالت آنلاین سرو می‌کند
 * - با بستن همه تب‌های سایت: کش پاک می‌شود
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
        if (extra) {
          for (var k in extra) msg[k] = extra[k];
        }
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
      .catch(function (err) {
        console.warn("[MCD offline] SW register failed", err);
        return null;
      });
  }

  function loadSitemapUrls() {
    return fetch(absoluteUrl("sitemap.xml"), { credentials: "same-origin", cache: "no-cache" })
      .then(function (r) {
        if (!r.ok) throw new Error("sitemap " + r.status);
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
      absoluteUrl("robots.txt"),
      absoluteUrl("python/"),
      absoluteUrl("html/"),
      absoluteUrl("css/"),
      absoluteUrl("javascript/"),
      absoluteUrl("php/"),
      absoluteUrl("tamrin/")
    ];
  }

  /* ---------- UI progress ---------- */
  function ensureBar() {
    var el = document.getElementById("mcd-offline-progress");
    if (el) return el;
    el = document.createElement("div");
    el.id = "mcd-offline-progress";
    el.setAttribute("role", "status");
    el.style.cssText = [
      "position:fixed",
      "bottom:16px",
      "left:50%",
      "transform:translateX(-50%)",
      "z-index:100000",
      "width:min(420px,92vw)",
      "padding:12px 14px",
      "border-radius:12px",
      "background:#0d1117",
      "color:#e6edf3",
      "border:1px solid #30363d",
      "font:13px/1.5 sans-serif",
      "box-shadow:0 10px 28px rgba(0,0,0,.4)",
      "text-align:center",
      "direction:rtl"
    ].join(";");
    el.innerHTML =
      '<div id="mcd-off-text">آماده‌سازی حالت آفلاین…</div>' +
      '<div style="margin-top:8px;height:6px;background:#21262d;border-radius:99px;overflow:hidden">' +
      '<div id="mcd-off-bar" style="height:100%;width:0%;background:#00e676;transition:width .2s"></div></div>';
    (document.body || document.documentElement).appendChild(el);
    return el;
  }

  function setProgress(done, total, label) {
    try {
      var wrap = ensureBar();
      var text = document.getElementById("mcd-off-text");
      var bar = document.getElementById("mcd-off-bar");
      var pct = total ? Math.min(100, Math.round((done / total) * 100)) : 0;
      if (text) {
        text.textContent =
          (label || "در حال ذخیره کل سایت") +
          " — " +
          done +
          " از " +
          total +
          " (" +
          pct +
          "٪)";
      }
      if (bar) bar.style.width = pct + "%";
      wrap.style.display = "block";
    } catch (e) {}
  }

  function hideProgress(finalMsg, ok) {
    try {
      var wrap = ensureBar();
      var text = document.getElementById("mcd-off-text");
      var bar = document.getElementById("mcd-off-bar");
      if (text) text.textContent = finalMsg;
      if (bar) {
        bar.style.width = "100%";
        bar.style.background = ok ? "#00e676" : "#f85149";
      }
      setTimeout(function () {
        wrap.style.opacity = "0";
        wrap.style.transition = "opacity .4s";
        setTimeout(function () {
          if (wrap.parentNode) wrap.parentNode.removeChild(wrap);
        }, 450);
      }, 3500);
    } catch (e) {}
  }

  /**
   * ذخیره واقعی همه URLها داخل Cache Storage
   * مستقیم از صفحه (قابل اعتمادتر از فقط پیام به SW)
   */
  function cacheAllUrls(urls) {
    if (!window.caches) {
      return Promise.reject(new Error("Cache API unsupported"));
    }

    var total = urls.length;
    var done = 0;
    var failed = [];
    var concurrency = 10;
    var index = 0;

    return caches.open(CACHE_NAME).then(function (cache) {
      function putOne(url) {
        return fetch(url, { credentials: "same-origin", cache: "no-cache" })
          .then(function (res) {
            if (!res || !res.ok) throw new Error("bad status");
            return cache.put(url, res).then(function () {
              /* نسخه با / و index.html برای لینک‌های داخلی */
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
            if (done % 15 === 0 || done === total) setProgress(done, total);
          })
          .catch(function () {
            failed.push(url);
            done += 1;
            if (done % 15 === 0 || done === total) setProgress(done, total);
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
        /* یک دور تلاش مجدد برای ناموفق‌ها */
        if (!failed.length) return { total: total, ok: total, fail: 0 };

        setProgress(0, failed.length, "تلاش مجدد فایل‌های باقی‌مانده");
        var retryList = failed.slice();
        failed = [];
        done = 0;
        total = retryList.length;
        index = 0;

        function putRetry(url) {
          return fetch(url, { credentials: "same-origin", cache: "no-cache" })
            .then(function (res) {
              if (!res || !res.ok) throw new Error("bad");
              return cache.put(url, res);
            })
            .then(function () {
              done += 1;
              setProgress(done, total, "تلاش مجدد");
            })
            .catch(function () {
              failed.push(url);
              done += 1;
              setProgress(done, total, "تلاش مجدد");
            });
        }

        function worker2() {
          if (index >= retryList.length) return Promise.resolve();
          var url = retryList[index++];
          return putRetry(url).then(worker2);
        }

        var workers2 = [];
        for (var w2 = 0; w2 < 6; w2++) workers2.push(worker2());
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
    if (fullPrefetchDone()) {
      hideProgress("سایت از قبل برای حالت آفلاین آماده است", true);
      return Promise.resolve();
    }
    if (!navigator.onLine) {
      hideProgress("آفلاین هستید — ابتدا با اینترنت وارد شوید تا کل سایت ذخیره شود", false);
      return Promise.resolve();
    }

    setProgress(0, 1, "خواندن فهرست تمام صفحات");

    return loadSitemapUrls()
      .catch(function () {
        return [];
      })
      .then(function (sitemapUrls) {
        var all = uniqueUrls(coreAssetUrls().concat(sitemapUrls));
        setProgress(0, all.length, "ذخیره " + all.length + " فایل روی دستگاه");

        return cacheAllUrls(all).then(function (stats) {
          markFullPrefetchDone();
          /* به SW هم خبر بده که از همین کش استفاده کند */
          notifySW("CACHE_READY", { total: stats.total, ok: stats.ok });

          if (stats.fail === 0) {
            hideProgress(
              "تمام " + stats.ok + " صفحه ذخیره شد — بدون اینترنت هم کامل کار می‌کند",
              true
            );
          } else {
            hideProgress(
              stats.ok +
                " صفحه ذخیره شد (" +
                stats.fail +
                " مورد رد شد) — بخش اصلی آفلاین آماده است",
              true
            );
          }
        });
      })
      .catch(function (err) {
        console.warn("[MCD offline] prefetch failed", err);
        hideProgress("خطا در ذخیره کامل سایت — صفحه را یک‌بار رفرش کنید", false);
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

    window.addEventListener("offline", function () {
      try {
        var t = document.createElement("div");
        t.textContent = "بدون اینترنت — سایت از حافظه دستگاه اجرا می‌شود";
        t.style.cssText =
          "position:fixed;bottom:18px;left:50%;transform:translateX(-50%);z-index:100001;padding:10px 14px;border-radius:10px;background:#0d1117;color:#00e676;border:1px solid #00e676;font:13px sans-serif;direction:rtl";
        document.body.appendChild(t);
        setTimeout(function () {
          if (t.parentNode) t.parentNode.removeChild(t);
        }, 4000);
      } catch (e) {}
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
        }, 400);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
