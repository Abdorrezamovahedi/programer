/* MCD offline — permanent cache
 * Online  → network first (fresh site)
 * Offline → cache first (saved site)
 * Cache is NOT cleared on leave; only replaced when user clears site data
 */
var CACHE = "mcd-offline-v4";

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
  "./assets/img/favicon.svg",
  "./404.html"
];

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
          /* drop only old mcd versions, keep v4 forever */
          if (key.indexOf("mcd-offline") === 0 && key !== CACHE) {
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

function matchInCache(cache, request) {
  return cache.match(request).then(function (hit) {
    if (hit) return hit;
    var url;
    try {
      url = new URL(request.url);
    } catch (e) {
      return null;
    }
    var path = url.pathname;
    var candidates = [url.origin + path];
    if (path.endsWith("/")) {
      candidates.push(url.origin + path + "index.html");
    } else if (!/\.\w+$/.test(path)) {
      candidates.push(url.origin + path + "/");
      candidates.push(url.origin + path + "/index.html");
    }
    if (path.endsWith("/index.html")) {
      candidates.push(url.origin + path.replace(/\/index\.html$/, "/"));
    }
    var chain = Promise.resolve(null);
    candidates.forEach(function (c) {
      chain = chain.then(function (prev) {
        return prev || cache.match(c);
      });
    });
    return chain;
  });
}

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (request.method !== "GET") return;
  if (!sameOrigin(request.url)) return;

  event.respondWith(
    caches.open(CACHE).then(function (cache) {
      return matchInCache(cache, request).then(function (cached) {
        /* OFFLINE → saved site only */
        if (!self.navigator.onLine) {
          if (cached) return cached;
          if (request.mode === "navigate") {
            return matchInCache(cache, new Request("./index.html")).then(function (home) {
              return home || cache.match("./404.html");
            });
          }
          return cached || Response.error();
        }

        /* ONLINE → real network, update cache quietly */
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
