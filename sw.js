/* MCD Code Up — offline service worker (GitHub Pages safe) */
var CACHE = 'mcd-offline-v3';

function scopeBase() {
  try {
    return self.registration && self.registration.scope
      ? self.registration.scope
      : self.location.href.replace(/sw\.js(?:\?.*)?$/i, '');
  } catch (e) {
    return self.location.origin + '/programer/';
  }
}

function assetList() {
  var base = scopeBase();
  if (base.slice(-1) !== '/') base += '/';
  return [
    base,
    base + 'index.html',
    base + 'offline.html',
    base + 'assets/css/main.css',
    base + 'assets/js/boot-loader.js',
    base + 'assets/js/app.js',
    base + 'assets/js/mcd-motion.js'
  ];
}

function offlineUrl() {
  var base = scopeBase();
  if (base.slice(-1) !== '/') base += '/';
  return base + 'offline.html';
}

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      var urls = assetList();
      return Promise.all(
        urls.map(function (u) {
          return cache.add(u).catch(function () {
            return null;
          });
        })
      ).then(function () {
        /* force offline page into cache even if others fail */
        return cache.add(offlineUrl()).catch(function () { return null; });
      });
    }).then(function () {
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.map(function (k) {
          if (k !== CACHE) return caches.delete(k);
        })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

self.addEventListener('fetch', function (event) {
  var req = event.request;
  if (req.method !== 'GET') return;

  event.respondWith(
    fetch(req)
      .then(function (res) {
        return res;
      })
      .catch(function () {
        return caches.match(req).then(function (cached) {
          if (cached) return cached;
          /* Any failed HTML/navigation → offline page from cache */
          return caches.match(offlineUrl()).then(function (off) {
            if (off) return off;
            return caches.match(new Request(offlineUrl())).then(function (off2) {
              if (off2) return off2;
              return new Response(
                '<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>اینترنت قطع است</title><style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#020805;color:#e8f5e9;font-family:Tahoma,sans-serif;text-align:center;padding:24px}h1{color:#00e676}</style></head><body><div><h1>اینترنت رو روشن کن دیگه</h1><p>بعد از وصل شدن، صفحه را رفرش کن.</p></div></body></html>',
                { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
              );
            });
          });
        });
      })
  );
});
