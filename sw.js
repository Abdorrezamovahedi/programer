/* MCD Code Up — full-site session offline cache
 * - Caches core assets on install
 * - Caches all pages when asked (CACHE_URLS)
 * - Serves from cache when offline
 * - Clears mcd-offline* caches when last tab leaves the site
 */
var CACHE = "mcd-offline-v2";
var CORE = [
  "./",
  "./index.html",
  "./assets/css/main.css",
  "./assets/js/boot-loader.js",
  "./assets/js/app.js",
  "./assets/js/home.js",
  "./assets/js/mcd-motion.js",
  "./assets/js/offline-session.js",
  "./assets/js/search.js",
  "./assets/js/exercises.js",
  "./assets/js/tamrin-filter.js",
  "./assets/img/favicon.svg",
  "./assets/img/og-default.svg",
  "./404.html",
  "./robots.txt",
  "./sitemap.xml"
];

var leaveTimer = null;
var openPages = 0;

function clearAllMcdCaches() {
  return caches.keys().then(function (keys) {
    return Promise.all(
      keys.map(function (key) {
        if (key.indexOf("mcd-offline") === 0) return caches.delete(key);
      })
    );
  });
}

function clientsCount() {
  return self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (list) {
    return list.length;
  });
}

function scheduleClearIfEmpty() {
  if (leaveTimer) clearTimeout(leaveTimer);
  leaveTimer = setTimeout(function () {
    clientsCount().then(function (n) {
      if (n === 0) {
        clearAllMcdCaches();
        openPages = 0;
      }
    });
  }, 1500);
}

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return Promise.all(
        CORE.map(function (u) {
          return cache.add(u).catch(function () {});
        })
      );
    }).then(function () {
      return self.skipWaiting();
    })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.map(function (key) {
          if (key !== CACHE && key.indexOf("mcd-offline") === 0) {
            return caches.delete(key);
          }
        })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

function sameOrigin(url) {
  try {
    return new URL(url).origin === self.location.origin;
  } catch (e) {
    return false;
  }
}

function isCacheableRequest(request) {
  if (request.method !== "GET") return false;
  if (!sameOrigin(request.url)) return false;
  if (request.url.indexOf("chrome-extension") !== -1) return false;
  return true;
}

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (!isCacheableRequest(request)) return;

  event.respondWith(
    caches.open(CACHE).then(function (cache) {
      return cache.match(request).then(function (cached) {
        var networkFetch = fetch(request)
          .then(function (response) {
            if (response && response.ok && (response.type === "basic" || response.type === "cors")) {
              try {
                cache.put(request, response.clone());
              } catch (e) {}
            }
            return response;
          })
          .catch(function () {
            if (cached) return cached;
            if (request.mode === "navigate") {
              return cache.match("./index.html").then(function (home) {
                return home || cache.match("./404.html");
              });
            }
            return cached;
          });

        if (cached) return cached;
        return networkFetch;
      });
    })
  );
});

self.addEventListener("message", function (event) {
  var data = event.data || {};

  if (data.type === "PAGE_SHOW") {
    openPages += 1;
    if (leaveTimer) {
      clearTimeout(leaveTimer);
      leaveTimer = null;
    }
  }

  if (data.type === "PAGE_HIDE" || data.type === "LEAVE_SITE") {
    openPages = Math.max(0, openPages - 1);
    scheduleClearIfEmpty();
  }

  if (data.type === "CLEAR_CACHE") {
    event.waitUntil(
      clearAllMcdCaches().then(function () {
        if (event.ports && event.ports[0]) event.ports[0].postMessage({ ok: true });
      })
    );
  }

  if (data.type === "CACHE_URLS" && Array.isArray(data.urls)) {
    event.waitUntil(
      caches.open(CACHE).then(function (cache) {
        var urls = data.urls.slice(0, 2500);
        var i = 0;
        var concurrency = 6;

        function next() {
          if (i >= urls.length) return Promise.resolve();
          var batch = [];
          for (var c = 0; c < concurrency && i < urls.length; c++, i++) {
            (function (url) {
              batch.push(
                fetch(url, { credentials: "same-origin" })
                  .then(function (res) {
                    if (res && res.ok) return cache.put(url, res);
                  })
                  .catch(function () {})
              );
            })(urls[i]);
          }
          return Promise.all(batch).then(next);
        }

        return next();
      }).then(function () {
        if (event.ports && event.ports[0]) {
          event.ports[0].postMessage({ ok: true, count: data.urls.length });
        }
      })
    );
  }
});
