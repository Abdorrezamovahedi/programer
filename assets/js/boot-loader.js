/**
 * MCD programmers – boot loader
 * First home visit: full (~2.2s). Lesson files: always ~0.25s.
 * One particle MCD only — no second logo/text.
 */
(function () {
  if (window.__MCD_BOOT_DONE__) return;
  window.__MCD_BOOT_DONE__ = true;

  function offlineUrl() {
    var path = (location.pathname || '').replace(/\\/g, '/');
    if (path.indexOf('/programer') !== -1) return '/programer/offline.html';
    if (/\/(python|html|css|javascript|php|tamrin)\//i.test(path)) {
      var segs = path.split('/').filter(Boolean);
      var i2 = -1;
      for (var k = 0; k < segs.length; k++) {
        if (/^(python|html|css|javascript|php|tamrin)$/i.test(segs[k])) { i2 = k; break; }
      }
      if (i2 >= 0) {
        var up2 = segs.length - i2;
        var d2 = [];
        for (var t = 0; t < up2; t++) d2.push('..');
        return d2.join('/') + '/offline.html';
      }
    }
    return 'offline.html';
  }

  /* If user enters site without internet → offline page immediately */
  try {
    if (!navigator.onLine && !/offline\.html$/i.test(location.pathname || '')) {
      try { sessionStorage.setItem('mcd_last_url', location.href); } catch (e) {}
      location.replace(offlineUrl());
      return;
    }
  } catch (e) {}

  /* Service worker registration */
  try {
    if ('serviceWorker' in navigator) {
      var swPath = 'sw.js';
      var path = (location.pathname || '').replace(/\\/g, '/');
      if (path.indexOf('/programer') !== -1) {
        swPath = '/programer/sw.js';
      } else if (/\/(python|html|css|javascript|php|tamrin)\//i.test(path)) {
        var parts = path.split('/').filter(Boolean);
        var idx = -1;
        for (var i = 0; i < parts.length; i++) {
          if (/^(python|html|css|javascript|php|tamrin)$/i.test(parts[i])) { idx = i; break; }
        }
        if (idx >= 0) {
          var up = parts.length - idx;
          var dots = [];
          for (var j = 0; j < up; j++) dots.push('..');
          swPath = dots.join('/') + '/sw.js';
        }
      }
      navigator.serviceWorker.register(swPath).catch(function () {});
    }
  } catch (e) {}

  /* While browsing: if net drops → offline page */
  try {
    if (!/offline\.html$/i.test(location.pathname || '')) {
      try { sessionStorage.setItem('mcd_last_url', location.href); } catch (e) {}
      window.addEventListener('offline', function () {
        try { sessionStorage.setItem('mcd_last_url', location.href); } catch (e) {}
        location.href = offlineUrl();
      });
    }
  } catch (e) {}

  /* Tidy line-by-line layout */
  try {
    if (!document.getElementById('mcd-line-exp-inline')) {
      var s = document.createElement('style');
      s.id = 'mcd-line-exp-inline';
      s.textContent =
        '.example-unit{margin:1rem 0 1.25rem}' +
        '.example-unit .codewrap{margin:0}' +
        '.example-unit .code,.codewrap>.code{margin-bottom:.5rem}' +
        '.line-exp,.exp.line-exp{margin:.55rem 0 0!important;padding:.75rem .85rem .85rem!important;border-radius:12px!important;background:#06120c!important;border:1px solid #1a3328!important;border-right:3px solid #00e676!important;color:#c8e6c9!important;animation:none!important;box-shadow:none!important}' +
        '.line-exp .exp-title{margin:0 0 .65rem!important;padding:0 0 .45rem!important;border-bottom:1px solid #1f3d2e!important;color:#00e676!important;font-weight:700!important;font-size:.88rem!important;line-height:1.4!important}' +
        '.line-exp .exp-title::before{content:none!important}' +
        '.line-exp-list{list-style:none!important;margin:0!important;padding:0!important;display:flex!important;flex-direction:column!important;gap:.5rem!important}' +
        '.line-exp-list li{display:grid!important;grid-template-columns:3.1rem 1fr!important;grid-template-areas:"num code" "num exp"!important;column-gap:.55rem!important;row-gap:.2rem!important;margin:0!important;padding:.55rem .65rem!important;border-radius:10px!important;background:#040d09!important;border:1px solid #163326!important;align-items:start!important}' +
        '.line-exp-list .ln{grid-area:num!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;min-width:2.85rem!important;height:1.55rem!important;margin:.1rem 0 0!important;padding:0 .4rem!important;border-radius:999px!important;background:rgba(0,230,118,.1)!important;border:1px solid rgba(0,230,118,.28)!important;color:#00e676!important;font-weight:700!important;font-size:.72rem!important;white-space:nowrap!important}' +
        '.line-exp-list .ln-code{grid-area:code!important;direction:ltr!important;unicode-bidi:plaintext!important;display:inline-block!important;max-width:100%!important;width:fit-content!important;margin:0!important;padding:.15rem .45rem!important;border-radius:6px!important;border:1px solid #243f32!important;background:#020805!important;color:#b2dfdb!important;font-family:ui-monospace,Consolas,monospace!important;font-size:.8rem!important;line-height:1.45!important;white-space:pre-wrap!important;word-break:break-word!important;box-shadow:none!important}' +
        '.line-exp-list .ln-exp{grid-area:exp!important;display:block!important;margin:0!important;padding:.05rem 0 0!important;color:#c8e6c9!important;font-size:.9rem!important;line-height:1.7!important}' +
        '@media (max-width:640px){.line-exp-list li{grid-template-columns:1fr!important;grid-template-areas:"num" "code" "exp"!important;row-gap:.28rem!important}.line-exp-list .ln{width:fit-content!important;margin:0!important}}';
      document.head.appendChild(s);
    }
  } catch (e) {}

  var mcdBootTier = "high";
  try {
    var __c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (__c) {
      if (__c.saveData) mcdBootTier = "low";
      else {
        var __t = String(__c.effectiveType || "").toLowerCase();
        if (__t === "slow-2g" || __t === "2g") mcdBootTier = "low";
        else if (__t === "3g") mcdBootTier = "mid";
      }
    }
  } catch (e) {}

  var FULL_MS = 1800;
  var LESSON_MS = 350;
  var FLAG = "mcd_boot_seen";

  function isLessonPage() {
    var path = (location.pathname || "").replace(/\\/g, "/");
    if (/\/index\.html?$/i.test(path) || /\/$/.test(path)) return false;
    if (/\/(python|html|css|javascript|php|tamrin)\//i.test(path)) {
      if (/\/index\.html?$/i.test(path)) return false;
      return true;
    }
    return false;
  }

  var isLesson = isLessonPage();
  var isShort = isLesson;
  if (!isLesson) {
    try { isShort = sessionStorage.getItem(FLAG) === "1"; } catch (e) {}
  }

  var DUR = isShort ? (mcdBootTier==="low"?200:LESSON_MS) : (mcdBootTier==="low"?900:mcdBootTier==="mid"?1400:FULL_MS);
  var CHARS = "01<>{}[]/+*=#";

  var css = document.createElement("style");
  css.id = "boot-loader-css";
  css.textContent =
    "#boot-loader{position:fixed;inset:0;background:#050505;z-index:99999;display:flex;align-items:center;justify-content:center;transition:opacity .35s ease,visibility .35s}" +
    "#boot-loader.hidden{opacity:0;visibility:hidden;pointer-events:none}" +
    "#boot-loader canvas{position:absolute;inset:0;width:100%;height:100%}";
  document.head.appendChild(css);

  var loader = document.createElement("div");
  loader.id = "boot-loader";
  loader.innerHTML = '<canvas id="boot-c"></canvas>';

  function mount() {
    if (!document.body) {
      document.addEventListener("DOMContentLoaded", mount);
      return;
    }
    document.body.insertBefore(loader, document.body.firstChild);
    start();
  }

  function finish() {
    if (!isLesson) {
      try { sessionStorage.setItem(FLAG, "1"); } catch (e) {}
    }
    if (!loader || loader.classList.contains("hidden")) return;
    loader.classList.add("hidden");
    setTimeout(function () {
      if (loader && loader.parentNode) loader.parentNode.removeChild(loader);
    }, isShort ? 200 : 400);
  }

  function start() {
    var canvas = document.getElementById("boot-c");
    if (!canvas) { finish(); return; }
    var ctx = canvas.getContext("2d", { alpha: false });
    var W = 0, H = 0, dpr = 1, parts = null, t0 = 0;

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth;
      H = window.innerHeight;
      canvas.width = (W * dpr) | 0;
      canvas.height = (H * dpr) | 0;
      canvas.style.width = W + "px";
      canvas.style.height = H + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    window.addEventListener("resize", resize);
    resize();

    function buildPoints() {
      var off = document.createElement("canvas");
      var ow = 520, oh = 180;
      off.width = ow; off.height = oh;
      var o = off.getContext("2d");
      o.fillStyle = "#000";
      o.fillRect(0, 0, ow, oh);
      o.fillStyle = "#fff";
      o.textAlign = "center";
      o.textBaseline = "middle";
      o.font = "bold 120px Arial Black, Arial, sans-serif";
      o.fillText("MCD", ow / 2, oh * 0.5);
      var data = o.getImageData(0, 0, ow, oh).data;
      var pts = [], step = isShort ? 8 : 5;
      for (var y = 0; y < oh; y += step) {
        for (var x = 0; x < ow; x += step) {
          if (data[(y * ow + x) * 4] > 140) pts.push({ nx: x / ow - 0.5, ny: y / oh - 0.5 });
        }
      }
      return pts;
    }

    function init() {
      var pts = buildPoints();
      var scaleX = Math.min(W * 0.75, 480);
      var scaleY = scaleX * 0.38;
      var cy = H * 0.48;
      parts = pts.map(function (p) {
        var ang = Math.random() * 6.2832;
        var dist = Math.max(W, H) * (0.22 + Math.random() * (isShort ? 0.18 : 0.5));
        return {
          x: W * 0.5 + Math.cos(ang) * dist,
          y: H * 0.5 + Math.sin(ang) * dist,
          tx: W * 0.5 + p.nx * scaleX,
          ty: cy + p.ny * scaleY,
          ch: CHARS[(Math.random() * CHARS.length) | 0],
          a: 0.5 + Math.random() * 0.4,
          d: Math.random() * (isShort ? 0.04 : 0.18)
        };
      });
    }

    function ease(t) { return t * (2 - t); }

    function frame(now) {
      if (!t0) t0 = now;
      var p = Math.min(1, (now - t0) / DUR);
      ctx.fillStyle = "#050505";
      ctx.fillRect(0, 0, W, H);
      ctx.font = '11px monospace';
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      for (var i = 0; i < parts.length; i++) {
        var pt = parts[i];
        var t = (p - pt.d) / (1 - pt.d);
        if (t < 0) t = 0; else if (t > 1) t = 1;
        t = ease(t);
        ctx.globalAlpha = pt.a * (0.2 + 0.8 * t);
        ctx.fillStyle = t > 0.82 ? "#00e676" : "#00c853";
        ctx.fillText(pt.ch, pt.x + (pt.tx - pt.x) * t, pt.y + (pt.ty - pt.y) * t);
      }
      ctx.globalAlpha = 1;
      if (p < 1) requestAnimationFrame(frame);
      else setTimeout(finish, isShort ? 60 : 250);
    }

    try {
      init();
      requestAnimationFrame(frame);
    } catch (e) {
      finish();
    }
    setTimeout(finish, DUR + (isShort ? 500 : 3500));
  }

  mount();
})();
