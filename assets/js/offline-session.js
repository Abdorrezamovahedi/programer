/**
 * MCD Code Up — verified offline pack manager
 * Manifest = sitemap pages + real static assets (from repo inventory)
 * cached ONLY after fetch OK + cache.put + cache.match verify
 * Progress = verifiedCached / total ; IndexedDB resume
 */
(function () {
  if (window.__MCD_OFFLINE_INIT__) return;
  window.__MCD_OFFLINE_INIT__ = true;

  var CACHE_NAME = "mcd-offline-v5";
  var DB_NAME = "mcd_offline_db_v5";
  var DB_VER = 1;
  var MANIFEST_VERSION = "2026-11-10-v1";
  var MAX_ATTEMPTS = 3;

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
    "index.html",
    "404.html",
    "sw.js",
    "robots.txt",
    "sitemap.xml",
    "offline-manifest-meta.json",
    "assets/css/main.css",
    "assets/js/boot-loader.js",
    "assets/js/app.js",
    "assets/js/home.js",
    "assets/js/mcd-motion.js",
    "assets/js/offline-session.js",
    "assets/js/search.js",
    "assets/js/exercises.js",
    "assets/js/tamrin-filter.js",
    "assets/img/favicon.svg",
    "assets/img/og-default.svg"
  ];

  var state = {
    total: 0,
    cached: 0,
    failed: 0,
    pending: 0,
    downloading: 0,
    running: false,
    resources: [],
    byPath: {},
    stopFlag: false
  };

  function absUrl(rel) {
    try {
      return new URL(String(rel).replace(/^\//, ""), location.origin + SCOPE_BASE).href;
    } catch (e) {
      return location.origin + SCOPE_BASE + String(rel).replace(/^\//, "");
    }
  }

  function classify(p) {
    var pl = String(p).toLowerCase();
    if (/\.html?$/.test(pl)) return "html";
    if (/\.css$/.test(pl)) return "css";
    if (/\.js$/.test(pl)) return "js";
    if (/\.(png|jpe?g|webp|gif|svg|ico)$/.test(pl)) return "image";
    if (/\.(woff2?|ttf|otf)$/.test(pl)) return "font";
    if (/\.(xml|txt|json)$/.test(pl)) return "data";
    return "other";
  }

  function openDb() {
    return new Promise(function (resolve, reject) {
      if (!window.indexedDB) {
        reject(new Error("no indexedDB"));
        return;
      }
      var req = indexedDB.open(DB_NAME, DB_VER);
      req.onupgradeneeded = function () {
        var db = req.result;
        if (!db.objectStoreNames.contains("files")) db.createObjectStore("files", { keyPath: "path" });
        if (!db.objectStoreNames.contains("meta")) db.createObjectStore("meta", { keyPath: "key" });
      };
      req.onsuccess = function () {
        resolve(req.result);
      };
      req.onerror = function () {
        reject(req.error || new Error("idb open fail"));
      };
    });
  }

  function idbGetAll(store) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, "readonly");
        var req = tx.objectStore(store).getAll();
        req.onsuccess = function () {
          resolve(req.result || []);
        };
        req.onerror = function () {
          reject(req.error);
        };
      });
    });
  }

  function idbPut(store, value) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(store, "readwrite");
        tx.objectStore(store).put(value);
        tx.oncomplete = function () {
          resolve();
        };
        tx.onerror = function () {
          reject(tx.error);
        };
      });
    });
  }

  function idbGetMeta(key) {
    return openDb().then(function (db) {
      return new Promise(function (resolve) {
        var tx = db.transaction("meta", "readonly");
        var req = tx.objectStore("meta").get(key);
        req.onsuccess = function () {
          resolve(req.result ? req.result.value : null);
        };
        req.onerror = function () {
          resolve(null);
        };
      });
    });
  }

  function idbSetMeta(key, value) {
    return idbPut("meta", { key: key, value: value });
  }

  function profileNetwork() {
    var level = "mid";
    try {
      var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (c) {
        if (c.saveData) return { level: "off", concurrency: 0, pauseMs: 0 };
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
    var cfg = map[level] || map.mid;
    return { level: level, concurrency: cfg.concurrency, pauseMs: cfg.pauseMs };
  }

  var ui = null;
  function ensureUI() {
    if (ui) return ui;
    ui = document.createElement("div");
    ui.id = "mcd-offline-panel";
    ui.setAttribute("dir", "rtl");
    ui.style.cssText =
      "position:fixed;bottom:12px;left:12px;z-index:99980;width:min(300px,92vw);" +
      "background:#0d1117;border:1px solid #238636;border-radius:12px;padding:10px 12px;" +
      "color:#e6edf3;font:12px/1.5 system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.35);display:none";
    ui.innerHTML =
      '<div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:6px">' +
      '<b style="color:#00e676">دانلود آفلاین</b>' +
      '<button type="button" id="mcd-off-toggle" style="background:transparent;border:0;color:#8b949e;cursor:pointer;font-size:14px">×</button></div>' +
      '<div id="mcd-off-status" style="color:#8b949e;margin-bottom:6px">آماده</div>' +
      '<div style="height:6px;background:#21262d;border-radius:99px;overflow:hidden;margin-bottom:6px">' +
      '<div id="mcd-off-bar" style="height:100%;width:0%;background:#00e676;transition:width .2s"></div></div>' +
      '<div id="mcd-off-nums" style="color:#8b949e;margin-bottom:8px">۰ / ۰</div>' +
      '<div style="display:flex;gap:6px;flex-wrap:wrap">' +
      '<button type="button" id="mcd-off-start" style="background:#238636;color:#fff;border:0;border-radius:8px;padding:6px 10px;cursor:pointer">شروع / ادامه</button>' +
      '<button type="button" id="mcd-off-pause" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:8px;padding:6px 10px;cursor:pointer">توقف</button>' +
      '<button type="button" id="mcd-off-retry" style="background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:8px;padding:6px 10px;cursor:pointer">تلاش مجدد ناموفق‌ها</button></div>';
    (document.body || document.documentElement).appendChild(ui);

    var fab = document.createElement("button");
    fab.id = "mcd-offline-fab";
    fab.type = "button";
    fab.textContent = "↓ آفلاین";
    fab.style.cssText =
      "position:fixed;bottom:12px;left:12px;z-index:99979;background:#0d1117;color:#00e676;" +
      "border:1px solid #238636;border-radius:999px;padding:8px 12px;font:12px system-ui;cursor:pointer";
    fab.onclick = function () {
      ui.style.display = "block";
      fab.style.display = "none";
    };
    (document.body || document.documentElement).appendChild(fab);

    document.getElementById("mcd-off-toggle").onclick = function () {
      ui.style.display = "none";
      fab.style.display = "block";
    };
    document.getElementById("mcd-off-start").onclick = function () {
      startDownload(false);
    };
    document.getElementById("mcd-off-pause").onclick = function () {
      state.stopFlag = true;
      state.running = false;
      renderUI("متوقف شد");
    };
    document.getElementById("mcd-off-retry").onclick = function () {
      startDownload(true);
    };
    return ui;
  }

  function renderUI(statusText) {
    try {
      ensureUI();
      var pct = state.total ? Math.floor((state.cached / state.total) * 100) : 0;
      var bar = document.getElementById("mcd-off-bar");
      var nums = document.getElementById("mcd-off-nums");
      var st = document.getElementById("mcd-off-status");
      if (bar) bar.style.width = pct + "%";
      if (nums)
        nums.textContent =
          "تأییدشده: " +
          state.cached +
          " / " +
          state.total +
          " (" +
          pct +
          "٪) · ناموفق: " +
          state.failed +
          " · مانده: " +
          state.pending;
      if (st) {
        if (statusText) st.textContent = statusText;
        else if (state.cached === state.total && state.total > 0 && state.failed === 0)
          st.textContent = "دانلود کامل و تأیید شد";
        else if (state.failed > 0 && state.pending === 0 && !state.running)
          st.textContent = "دانلود ناقص — نیاز به تلاش مجدد";
        else if (state.running) st.textContent = "در حال دانلود و تأیید…";
        else st.textContent = "آماده";
      }
    } catch (e) {}
  }

  function recount() {
    var c = 0,
      f = 0,
      p = 0,
      d = 0;
    for (var i = 0; i < state.resources.length; i++) {
      var s = state.resources[i].status;
      if (s === "cached") c++;
      else if (s === "failed") f++;
      else if (s === "downloading" || s === "retrying") d++;
      else p++;
    }
    state.cached = c;
    state.failed = f;
    state.pending = p;
    state.downloading = d;
  }

  function cacheOneVerified(path) {
    var url = absUrl(path);
    return fetch(url, { credentials: "same-origin", cache: "no-cache" })
      .then(function (res) {
        if (!res) throw { code: "network", message: "empty response" };
        if (!res.ok) throw { code: "http", message: "HTTP " + res.status };
        if (res.type === "opaque") throw { code: "opaque", message: "opaque response" };
        if (res.status === 206) throw { code: "partial", message: "partial content not accepted" };
        return res.blob().then(function (blob) {
          var putRes = new Response(blob, {
            status: res.status,
            statusText: res.statusText,
            headers: res.headers
          });
          return caches.open(CACHE_NAME).then(function (cache) {
            return cache.put(url, putRes).then(function () {
              return cache.match(url).then(function (matched) {
                if (!matched) throw { code: "verify", message: "cache.match failed after put" };
                return true;
              });
            });
          });
        });
      })
      .catch(function (err) {
        if (err && err.name === "QuotaExceededError") throw { code: "quota", message: "storage full" };
        if (err && err.code) throw err;
        throw { code: "network", message: String((err && err.message) || err || "fetch failed") };
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
    } catch (e) {
      return null;
    }
  }

  function loadManifest() {
    var metaP = fetch(absUrl("offline-manifest-meta.json"), {
      credentials: "same-origin",
      cache: "no-cache"
    })
      .then(function (r) {
        return r.ok ? r.json() : {};
      })
      .catch(function () {
        return {};
      });

    var mapP = fetch(absUrl("sitemap.xml"), {
      credentials: "same-origin",
      cache: "no-cache"
    })
      .then(function (r) {
        if (!r.ok) throw new Error("sitemap");
        return r.text();
      })
      .then(function (xml) {
        var urls = [];
        var re = /<loc>\s*([^<]+)\s*<\/loc>/gi;
        var m;
        while ((m = re.exec(xml))) urls.push(m[1].trim());
        return urls;
      })
      .catch(function () {
        return [];
      });

    return Promise.all([metaP, mapP]).then(function (pair) {
      var meta = pair[0] || {};
      var locs = pair[1] || [];
      if (meta.version) MANIFEST_VERSION = meta.version;
      if (meta.cacheName) CACHE_NAME = meta.cacheName;

      var seen = {};
      var resources = [];
      function add(path) {
        if (!path || seen[path]) return;
        seen[path] = 1;
        resources.push({ p: path, t: classify(path) });
      }

      for (var i = 0; i < STATIC_ASSETS.length; i++) add(STATIC_ASSETS[i]);
      for (var j = 0; j < locs.length; j++) {
        var p = pathFromLoc(locs[j]);
        if (p) add(p);
      }

      return {
        version: MANIFEST_VERSION,
        cacheName: CACHE_NAME,
        total: resources.length,
        resources: resources,
        stats: meta.stats || null
      };
    });
  }

  function hydrate(manifest) {
    MANIFEST_VERSION = manifest.version || MANIFEST_VERSION;
    if (manifest.cacheName) CACHE_NAME = manifest.cacheName;
    var list = (manifest.resources || []).map(function (r) {
      return {
        path: r.p || r.path,
        type: r.t || r.type || "other",
        status: "pending",
        attempts: 0,
        error: null
      };
    });
    state.resources = list;
    state.total = list.length;
    state.byPath = {};
    for (var i = 0; i < list.length; i++) state.byPath[list[i].path] = list[i];

    return idbGetMeta("manifestVersion")
      .then(function (prevVer) {
        return idbGetAll("files").then(function (rows) {
          if (prevVer && prevVer === MANIFEST_VERSION && rows && rows.length) {
            for (var j = 0; j < rows.length; j++) {
              var row = rows[j];
              var item = state.byPath[row.path];
              if (item) {
                item.status = row.status || "pending";
                item.attempts = row.attempts || 0;
                item.error = row.error || null;
                if (item.status === "downloading" || item.status === "retrying") item.status = "pending";
              }
            }
          }
          return idbSetMeta("manifestVersion", MANIFEST_VERSION);
        });
      })
      .then(function () {
        recount();
        renderUI();
      });
  }

  function persistItem(item) {
    return idbPut("files", {
      path: item.path,
      status: item.status,
      attempts: item.attempts,
      error: item.error,
      updatedAt: Date.now()
    });
  }

  function pickNext(retryOnly) {
    for (var i = 0; i < state.resources.length; i++) {
      var it = state.resources[i];
      if (retryOnly) {
        if (it.status === "failed" && it.attempts < MAX_ATTEMPTS) return it;
      } else if (it.status === "pending" || it.status === "failed") return it;
    }
    return null;
  }

  function startDownload(retryOnly) {
    if (state.running) return;
    if (!navigator.onLine) {
      renderUI("آفلاین هستید — فقط صفحات ذخیره‌شده در دسترس‌اند");
      return;
    }
    state.stopFlag = false;
    state.running = true;
    renderUI("در حال دانلود و تأیید…");

    var profile = profileNetwork();
    if (profile.level === "off" || profile.concurrency < 1) {
      state.running = false;
      renderUI("حالت صرفه‌جویی اینترنت فعال است");
      return;
    }

    var active = 0;
    var concurrency = profile.concurrency;

    function pump() {
      if (state.stopFlag) {
        state.running = false;
        renderUI("متوقف شد");
        return;
      }
      while (active < concurrency) {
        var item = pickNext(retryOnly);
        if (!item) break;
        active++;
        item.status = item.attempts > 0 ? "retrying" : "downloading";
        item.attempts += 1;
        persistItem(item);
        recount();
        renderUI();

        (function (current) {
          cacheOneVerified(current.path)
            .then(function () {
              current.status = "cached";
              current.error = null;
              return persistItem(current);
            })
            .catch(function (err) {
              current.error =
                (err && err.code ? err.code + ": " : "") + ((err && err.message) || "error");
              current.status = "failed";
              return persistItem(current);
            })
            .then(function () {
              active--;
              recount();
              renderUI();
              setTimeout(pump, profile.pauseMs || 0);
            });
        })(item);
      }

      if (active === 0) {
        state.running = false;
        recount();
        if (state.cached === state.total && state.failed === 0) {
          renderUI("دانلود کامل و تأیید شد");
          idbSetMeta("complete", true);
        } else if (state.failed > 0) {
          renderUI("دانلود ناقص — " + state.failed + " فایل ناموفق");
        } else {
          renderUI("آماده");
        }
      }
    }

    pump();
  }

  function registerSW() {
    if (!("serviceWorker" in navigator)) return Promise.resolve(null);
    var swUrl = (SCOPE_BASE + "sw.js").replace(/([^:]\/)\/+/g, "$1");
    return navigator.serviceWorker.register(swUrl, { scope: SCOPE_BASE }).catch(function () {
      return null;
    });
  }

  function init() {
    ensureUI();
    registerSW()
      .then(function () {
        return loadManifest();
      })
      .then(function (manifest) {
        return hydrate(manifest);
      })
      .then(function () {
        if (state.cached < state.total && navigator.onLine) {
          setTimeout(function () {
            if (!state.running && state.cached < state.total) startDownload(false);
          }, isMobile ? 10000 : 6000);
        }
      })
      .catch(function (err) {
        console.warn("[MCD offline]", err);
        renderUI("خطا در بارگذاری فهرست آفلاین");
      });
  }

  if (document.readyState === "complete") init();
  else window.addEventListener("load", init);
})();
