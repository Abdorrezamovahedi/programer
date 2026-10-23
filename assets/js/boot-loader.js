/**
 * MCD programmers – boot loader
 * First home visit: full (~2.2s). Lesson files: always ~0.25s.
 * One particle MCD only — no second logo/text.
 */
(function () {
  if (window.__MCD_BOOT_DONE__) return;
  window.__MCD_BOOT_DONE__ = true;

  var FULL_MS = 2200;
  var LESSON_MS = 250;
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

  var DUR = isShort ? LESSON_MS : FULL_MS;
  var CHARS = "01<>{}[]/+*=#";

  var css = document.createElement("style");
  css.id = "boot-loader-css";
  css.textContent =
    "#boot-loader{position:fixed;inset:0;background:#050505;z-index:99999;display:flex;align-items:center;justify-content:center;transition:opacity .35s ease,visibility .35s}" +
    "#boot-loader.hidden{opacity:0;visibility:hidden;pointer-events:none}" +
    "#boot-loader canvas{position:absolute;inset:0;width:100%;height:100%}";
  document.head.appendChild(css);

  if (!document.getElementById("mcd-boot-fonts")) {
    var fl = document.createElement("link");
    fl.id = "mcd-boot-fonts";
    fl.rel = "stylesheet";
    fl.href = "https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Fira+Code:wght@500&display=swap";
    document.head.appendChild(fl);
  }

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
      o.font = "bold 120px Orbitron, Arial Black, sans-serif";
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
      ctx.font = '11px "Fira Code", monospace';
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
    setTimeout(finish, DUR + (isShort ? 600 : 3500));
  }

  mount();
})();
