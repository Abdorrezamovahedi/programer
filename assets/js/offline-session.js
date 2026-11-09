/**
 * MCD permanent offline pack — adaptive to real network quality
 *
 * Measures connection (API + small probe) and chooses batch size / pause:
 *   very-slow / save-data → almost idle, tiny batches
 *   slow                 → calm
 *   mid                  → balanced
 *   fast                 → quicker fill, still background priority:low
 *
 * Cache stays forever after first complete fill.
 * Online = live site; Offline = saved pack.
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

  /**
   * Profile network → { level, batchSize, pauseMs, startDelay }
   * level: off | very-slow | slow | mid | fast
   */
  function profileNetwork() {
    var level = "mid";
    var downlink = null;
    var rtt = null;
    var effective = "";
    var saveData = false;

    try {
      var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (c) {
        saveData = !!c.saveData;
        effective = String(c.effectiveType || "").toLowerCase();
        if (typeof c.downlink === "number") downlink = c.downlink;
        if (typeof c.rtt === "number") rtt = c.rtt;
      }
    } catch (e) {}

    if (saveData) {
      level = "off";
    } else if (effective === "slow-2g" || effective === "2g") {
      level = "very-slow";
    } else if (effective === "3g") {
      level = "slow";
    } else if (effective === "4g") {
      level = "fast";
    }

    if (downlink != null) {
      if (downlink > 0 && downlink < 0.5) level = "very-slow";
      else if (downlink < 1.5 && level === "fast") level = "slow";
      else if (downlink < 3 && level === "fast") level = "mid";
      else if (downlink >= 8) level = "fast";
    }

    if (rtt != null) {
      if (rtt >= 800) level = level === "fast" ? "slow" : "very-slow";
      else if (rtt >= 400 && level === "fast") level = "mid";
    }

    /* mobile is a bit more conservative */
    if (isMobile && level === "fast") level = "mid";

    var table = {
      off: { batchSize: 0, pauseMs: 0, startDelay: 0 },
      "very-slow": { batchSize: 1, pauseMs: 2000, startDelay: isMobile ? 12000 : 8000 },
      slow: { batchSize: 2, pauseMs: 1200, startDelay: isMobile ? 10000 : 6000 },
      mid: { batchSize: isMobile ? 3 : 6, pauseMs: isMobile ? 800 : 350, startDelay: isMobile ? 7000 : 4000 },
      fast: { batchSize: isMobile ? 5 : 10, pauseMs: isMobile ? 400 : 150, startDelay: isMobile ? 5000 : 3000 }
    };

    var cfg = table[level] || table.mid;
    return {
      level: level,
      batchSize: cfg.batchSize,
      pauseMs: cfg.pauseMs,
      startDelay: cfg.startDelay,
      downlink: downlink,
      rtt: rtt,
      effective: effective
    };
  }

  /** Optional real probe: time a small same-origin file */
  function probeSpeed(baseProfile) {
    return new Promise(function (resolve) {
      var url = absoluteUrl("assets/img/favicon.svg") + "?probe=" + Date.now();
      var t0 = performance.now ? performance.now() : Date.now();
      var settled = false;
      function done(p) {
        if (settled) return;
        settled = true;
        resolve(p);
      }
      setTimeout(function () {
        done(baseProfile);
      }, 2500);

      fetch(url, { credentials: "same-origin", cache: "no-store", priority: "low" })
        .then(function (res) {
          return res.arrayBuffer().then(function (buf) {
            var t1 = performance.now ? performance.now() : Date.now();
            var ms = Math.max(1, t1 - t0);
            var bytes = buf ? buf.byteLength : 0;
            var kbps = bytes > 0 ? (bytes * 8) / ms : 0; /* approx kilobits/ms → scale */
            /* normalize: favicon is tiny; use latency mainly */
            var p = {
              level: baseProfile.level,
              batchSize: baseProfile.batchSize,
              pauseMs: baseProfile.pauseMs,
              startDelay: baseProfile.startDelay,
              downlink: baseProfile.downlink,
              rtt: baseProfile.rtt,
              effective: baseProfile.effective
            };
            if (ms > 1500) {
              p.level = "very-slow";
              p.batchSize = 1;
              p.pauseMs = 2200;
            } else if (ms > 800) {
              if (p.level === "fast") p.level = "mid";
              p.batchSize = Math.min(p.batchSize, isMobile ? 2 : 4);
              p.pauseMs = Math.max(p.pauseMs, 900);
            } else if (ms < 200 && p.level !== "off") {
              p.level = isMobile ? "mid" : "fast";
              p.batchSize = isMobile ? 5 : 10;
              p.pauseMs = isMobile ? 400 : 150;
            }
            done(p);
          });
        })
        .catch(function () {
          done(baseProfile);
        });
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

  function adaptiveFill(urls, profile) {
    if (!window.caches || !navigator.onLine) return Promise.resolve();
    if (profile.level === "off" || profile.batchSize < 1) return Promise.resolve();

    var batchSize = profile.batchSize;
    var pauseMs = profile.pauseMs;
    var cursor = getCursor();
    if (cursor >= urls.length) {
      markDone();
      return Promise.resolve();
    }

    return caches.open(CACHE_NAME).then(function (cache) {
      function runBatch() {
        if (!navigator.onLine) return Promise.resolve();

        /* re-check network each batch — adapt if user moved to worse signal */
        var live = profileNetwork();
        if (live.level === "off") return Promise.resolve();
        if (live.level === "very-slow") {
          batchSize = 1;
          pauseMs = Math.max(pauseMs, 2000);
        } else if (live.level === "slow") {
          batchSize = Math.min(batchSize, 2);
          pauseMs = Math.max(pauseMs, 1000);
        }

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

    var base = profileNetwork();
    if (base.level === "off") return; /* Save-Data: respect user, don't bulk download */

    probeSpeed(base).then(function (profile) {
      loadSitemapUrls()
        .catch(function () {
          return [];
        })
        .then(function (map) {
          var all = unique(coreUrls().concat(map));
          return adaptiveFill(all, profile);
        })
        .catch(function () {});
    });
  }

  function init() {
    registerSW().then(function () {
      var base = profileNetwork();
      var delay = base.startDelay || (isMobile ? 8000 : 5000);

      setTimeout(function () {
        if (typeof requestIdleCallback === "function") {
          requestIdleCallback(
            function () {
              startBackgroundPack();
            },
            { timeout: 6000 }
          );
        } else {
          startBackgroundPack();
        }
      }, delay);

      /* if network improves later, try continue (cursor resumes) */
      try {
        var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
        if (conn && conn.addEventListener) {
          conn.addEventListener("change", function () {
            if (!isDone() && navigator.onLine) {
              setTimeout(startBackgroundPack, 3000);
            }
          });
        }
      } catch (e) {}

      window.addEventListener("online", function () {
        if (!isDone()) setTimeout(startBackgroundPack, 2000);
      });
    });
  }

  if (document.readyState === "complete") init();
  else window.addEventListener("load", init);
})();
