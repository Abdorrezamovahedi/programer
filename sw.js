/* MCD SW v7 — Network First when online; Cache when offline */
var CACHE = "mcd-offline-v7";
var CORE = [
  "./",
  "./index.html",
  "./assets/css/main.css",
  "./assets/js/boot-loader.js",
  "./assets/js/app.js",
  "./assets/js/home.js",
  "./assets/img/favicon.svg",
  "./404.html",
  "./offline-manifest-meta.json"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return Promise.all(CORE.map(function (u) {
        return cache.add(u).catch(function () {});
      }));
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
          if (key !== CACHE) return caches.delete(key);
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
    if (path.endsWith("/")) candidates.push(url.origin + path + "index.html");
    else if (!/\.\w+$/.test(path)) {
      candidates.push(url.origin + path + "/");
      candidates.push(url.origin + path + "/index.html");
    }
    if (path.endsWith("/index.html"))
      candidates.push(url.origin + path.replace(/\/index\.html$/, "/"));
    var chain = Promise.resolve(null);
    candidates.forEach(function (c) {
      chain = chain.then(function (prev) {
        return prev || cache.match(c);
      });
    });
    return chain;
  });
}

function offlineFallback(cache, request) {
  return matchInCache(cache, request).then(function (hit) {
    if (hit) return hit;
    if (request.mode === "navigate") {
      return matchInCache(cache, new Request("./index.html")).then(function (home) {
        return (
          home ||
          cache.match("./404.html") ||
          new Response(
            "<!doctype html><html lang=fa dir=rtl><meta charset=utf-8><title>آفلاین</title>" +
              "<body style=\"font-family:system-ui;background:#0d1117;color:#e6edf3;padding:24px;text-align:center\">" +
              "<h1 style=\"color:#00e676\">این صفحه هنوز برای استفاده آفلاین ذخیره نشده است.</h1>" +
              "<p>برای دسترسی بدون اینترنت، ابتدا به اینترنت متصل شوید و این صفحه را دانلود کنید.</p>" +
              "</body></html>",
            { status: 503, headers: { "Content-Type": "text/html; charset=utf-8" } }
          )
        );
      });
    }
    return new Response("", { status: 503 });
  });
}

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (request.method !== "GET") return;
  if (!sameOrigin(request.url)) return;

  var isControlJs =
    /\/assets\/js\/(offline-session|boot-loader)\.js/.test(request.url) ||
    /\/sw\.js/.test(request.url);

  event.respondWith(
    (async function () {
      var cache = await caches.open(CACHE);

      /* Always try network first when possible */
      try {
        var response = await fetch(request, isControlJs ? { cache: "no-store" } : undefined);
        if (response && response.ok && (response.type === "basic" || response.type === "cors")) {
          try {
            if (!isControlJs) await cache.put(request, response.clone());
          } catch (ePut) {}
        }
        return response;
      } catch (err) {
        return offlineFallback(cache, request);
      }
    })()
  );
});
