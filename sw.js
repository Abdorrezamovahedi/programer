/* MCD Code Up — seamless full-site offline
 * When online: network first, update cache
 * When offline: cache first — site works as if still online
 * Full site is prefetched on first visit of the session
 * Cache cleared only when every site tab is closed
 */
var CACHE = "mcd-offline-v3";
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

/* Only clear after all windows are gone (not on app switch) */
function scheduleClearIfEmpty() {
  if (leaveTimer) clearTimeout(leaveTimer);
  leaveTimer = setTimeout(function () {
    clientsCount().then(function (n) {
      if (n === 0) clearAllMcdCaches();
    });
  }, 2500);
}

function cancelClear() {
  if (leaveTimer) {
    clearTimeout(leaveTimer);
    leaveTimer = null;
  }
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

/* Try several URL shapes so offline links always hit cache */
function matchInCache(cache, request) {
  return cache.match(request).then(function (hit) {
    if (hit) return hit;
    var url;
    try {
      url = new URL(request.url);
    } catch (e) {
      return null;
    }
    var candidates = [];
    var path = url.pathname;
    candidates.push(url.origin + path);
    if (path.endsWith("/")) {
      candidates.push(url.origin + path + "index.html");
    } else if (!/\.\w+$/.test(path)) {
      candidates.push(url.origin + path + "/");
      candidates.push(url.origin + path + "/index.html");
    }
    if (path.endsWith("/index.html")) {
      candidates.push(url.origin + path.replace(/\/index\.html$/, "/"));
      candidates.push(url.origin + path.replace(/\/index\.html$/, ""));
    }
    var chain = Promise.resolve(null);
    candidates.forEach(function (c) {
      chain = chain.then(function (prev) {
        if (prev) return prev;
        return cache.match(c);
      });
    });
    return chain;
  });
}

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (!isCacheableRequest(request)) return;

  event.respondWith(
    caches.open(CACHE).then(function (cache) {
      return matchInCache(cache, request).then(function (cached) {
        /* Offline → always prefer cache (feels like internet is still on) */
        if (!self.navigator.onLine) {
          if (cached) return cached;
          if (request.mode === "navigate") {
            return matchInCache(cache, new Request("./index.html")).then(function (home) {
              return home || cache.match("./404.html");
            });
          }
          return cached || Response.error();
        }

        /* Online → network first, keep cache fresh */
        return fetch(request)
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
              return matchInCache(cache, new Request("./index.html")).then(function (home) {
                return home || cache.match("./404.html");
              });
            }
            return cached || Response.error();
          });
      });
    })
  );
});

self.addEventListener("message", function (event) {
  var data = event.data || {};

  if (data.type === "PAGE_SHOW") {
    cancelClear();
  }

  if (data.type === "PAGE_HIDE" || data.type === "LEAVE_SITE") {
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
        var concurrency = 8;

        function next() {
          if (i >= urls.length) return Promise.resolve();
          var batch = [];
          for (var c = 0; c < concurrency && i < urls.length; c++, i++) {
            (function (url) {
              batch.push(
                fetch(url, { credentials: "same-origin" })
                  .then(function (res) {
                    if (res && res.ok) {
                      return cache.put(url, res).then(function () {
                        /* also store slash / index variants for navigations */
                        try {
                          var u = new URL(url);
                          if (u.pathname.endsWith("/index.html")) {
                            var dir = u.origin + u.pathname.replace(/\/index\.html$/, "/");
                            return fetch(url, { credentials: "same-origin" }).then(function (r2) {
                              if (r2 && r2.ok) return cache.put(dir, r2);
                            });
                          }
                        } catch (e) {}
                      });
                    }
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
