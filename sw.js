/* MCD offline service worker */
var CACHE = "mcd-offline-v1";
var ASSETS = [
  "./",
  "./index.html",
  "./offline.html",
  "./assets/css/main.css",
  "./assets/js/boot-loader.js",
  "./assets/js/mcd-motion.js"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(ASSETS).catch(function () {
        return cache.addAll(["./offline.html", "./index.html"]);
      });
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  var req = event.request;
  if (req.method !== "GET") return;

  event.respondWith(
    fetch(req).then(function (res) {
      return res;
    }).catch(function () {
      return caches.match(req).then(function (cached) {
        if (cached) return cached;
        if (req.mode === "navigate" || (req.headers.get("accept") || "").indexOf("text/html") !== -1) {
          return caches.match("./offline.html");
        }
        return caches.match("./offline.html");
      });
    })
  );
});
