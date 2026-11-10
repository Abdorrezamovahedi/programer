/* MCD SW v6 — drops old caches; offline-session always network when online */
var CACHE = "mcd-offline-v6";
var CORE = [
  "./",
  "./index.html",
  "./assets/css/main.css",
  "./assets/js/boot-loader.js",
  "./assets/js/app.js",
  "./assets/js/home.js",
  "./assets/img/favicon.svg",
  "./404.html"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return Promise.all(CORE.map(function (u) { return cache.add(u).catch(function () {}); }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (key) {
        if (key !== CACHE) return caches.delete(key);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

function sameOrigin(url) {
  try { return new URL(url).origin === self.location.origin; } catch (e) { return false; }
}

function matchInCache(cache, request) {
  return cache.match(request).then(function (hit) {
    if (hit) return hit;
    var url;
    try { url = new URL(request.url); } catch (e) { return null; }
    var path = url.pathname;
    var candidates = [url.origin + path];
    if (path.endsWith("/")) candidates.push(url.origin + path + "index.html");
    else if (!/\.\w+$/.test(path)) {
      candidates.push(url.origin + path + "/");
      candidates.push(url.origin + path + "/index.html");
    }
    if (path.endsWith("/index.html")) candidates.push(url.origin + path.replace(/\/index\.html$/, "/"));
    var chain = Promise.resolve(null);
    candidates.forEach(function (c) {
      chain = chain.then(function (prev) { return prev || cache.match(c); });
    });
    return chain;
  });
}

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (request.method !== "GET") return;
  if (!sameOrigin(request.url)) return;

  var isControlJs = /\/assets\/js\/(offline-session|boot-loader)\.js/.test(request.url) || /\/sw\.js/.test(request.url);

  event.respondWith((async function () {
    var cache = await caches.open(CACHE);
    var online = true;
    try { online = self.navigator.onLine !== false; } catch (e) { online = true; }

    if (!online) {
      var cachedOff = await matchInCache(cache, request);
      if (cachedOff) return cachedOff;
      if (request.mode === "navigate") {
        return (await matchInCache(cache, new Request("./index.html"))) ||
          (await cache.match("./404.html")) ||
          new Response("آفلاین — این صفحه هنوز ذخیره نشده", { status: 503, headers: { "Content-Type": "text/plain; charset=utf-8" } });
      }
      return new Response("", { status: 503 });
    }

    try {
      var response = await fetch(request, isControlJs ? { cache: "no-store" } : undefined);
      if (response && response.ok && (response.type === "basic" || response.type === "cors")) {
        try { if (!isControlJs) cache.put(request, response.clone()); } catch (e2) {}
      }
      return response;
    } catch (err) {
      var cached = await matchInCache(cache, request);
      if (cached) return cached;
      if (request.mode === "navigate") {
        return (await matchInCache(cache, new Request("./index.html"))) ||
          (await cache.match("./404.html")) || Response.error();
      }
      return Response.error();
    }
  })());
});
