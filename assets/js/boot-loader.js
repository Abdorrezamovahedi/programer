/**
 * MCD programmers – boot loader (original particle MCD animation)
 * Offline UI loads ONLY for app entry (?mcd=app / app.html), never Google site.
 */
(function () {
  if (window.__MCD_BOOT_DONE__) return;
  window.__MCD_BOOT_DONE__ = true;

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
    try {
      isShort = sessionStorage.getItem(FLAG) === "1";
    } catch (e) {}
  }

  var DUR = isShort
    ? mcdBootTier === "low"
      ? 200
      : LESSON_MS
    : mcdBootTier === "low"
      ? 900
      : mcdBootTier === "mid"
        ? 1400
        : FULL_MS;

  function mount() {
    var root = document.createElement("div");
    root.id = "mcd-boot";
    root.setAttribute("aria-hidden", "true");
    root.style.cssText =
      "position:fixed;inset:0;z-index:999999;background:#05080c;display:flex;" +
      "align-items:center;justify-content:center;transition:opacity .35s ease";

    var canvas = document.createElement("canvas");
    canvas.width = 320;
    canvas.height = 120;
    canvas.style.cssText = "max-width:90vw;height:auto";
    root.appendChild(canvas);
    document.documentElement.appendChild(root);

    var ctx = canvas.getContext("2d");
    var t0 = performance.now();
    var letters = ["M", "C", "D"];
    var particles = [];
    for (var i = 0; i < 48; i++) {
      particles.push({
        x: Math.random() * 320,
        y: Math.random() * 120,
        vx: (Math.random() - 0.5) * 1.2,
        vy: (Math.random() - 0.5) * 1.2,
        r: 1 + Math.random() * 2
      });
    }

    function frame(now) {
      var elapsed = now - t0;
      var p = Math.min(1, elapsed / DUR);
      ctx.clearRect(0, 0, 320, 120);
      ctx.fillStyle = "#00e676";
      for (var j = 0; j < particles.length; j++) {
        var pt = particles[j];
        pt.x += pt.vx;
        pt.y += pt.vy;
        if (pt.x < 0 || pt.x > 320) pt.vx *= -1;
        if (pt.y < 0 || pt.y > 120) pt.vy *= -1;
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, pt.r, 0, Math.PI * 2);
        ctx.globalAlpha = 0.35 + 0.4 * Math.sin(elapsed / 200 + j);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      ctx.font = "bold 48px Orbitron, system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "#00e676";
      ctx.shadowColor = "#00e676";
      ctx.shadowBlur = 12;
      var label = letters.slice(0, 1 + Math.floor(p * 2.99)).join("");
      ctx.fillText(label || "M", 160, 60);
      ctx.shadowBlur = 0;

      if (elapsed < DUR) {
        requestAnimationFrame(frame);
      } else {
        try {
          if (!isLesson) sessionStorage.setItem(FLAG, "1");
        } catch (e2) {}
        root.style.opacity = "0";
        setTimeout(function () {
          if (root.parentNode) root.parentNode.removeChild(root);
        }, 400);
      }
    }
    requestAnimationFrame(frame);
  }

  if (document.body) mount();
  else document.addEventListener("DOMContentLoaded", mount);

  /* Offline ONLY for app — NEVER on Google site */
  function isMcdAppEntry() {
    try {
      var q = location.search || "";
      var path = location.pathname || "";
      if (/[?&]mcd=app\b/i.test(q) || /\/app\.html$/i.test(path)) return true;
      if (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) return true;
      if (typeof navigator.standalone === "boolean" && navigator.standalone === true) return true;
      try {
        if (sessionStorage.getItem("mcd_app_mode") === "1") return true;
      } catch (e0) {}
    } catch (e) {}
    return false;
  }

  function loadOffline() {
    if (!isMcdAppEntry()) {
      try {
        sessionStorage.removeItem("mcd_app_mode");
        localStorage.removeItem("mcd_app_mode");
        localStorage.removeItem("mcd_is_app");
      } catch (eClr) {}
      return;
    }
    if (window.__MCD_OFFLINE_SCRIPT__) return;
    window.__MCD_OFFLINE_SCRIPT__ = true;
    try {
      sessionStorage.setItem("mcd_app_mode", "1");
    } catch (e1) {}
    try {
      var s = document.createElement("script");
      s.async = true;
      s.defer = true;
      s.src = (function () {
        var scripts = document.getElementsByTagName("script");
        for (var i = 0; i < scripts.length; i++) {
          var src = scripts[i].src || "";
          if (src.indexOf("boot-loader.js") !== -1) {
            return src.replace(/boot-loader\.js.*$/, "offline-session-v8.js");
          }
        }
        if ((location.pathname || "").indexOf("/programer") === 0) {
          return "/programer/assets/js/offline-session-v8.js";
        }
        return "assets/js/offline-session-v8.js";
      })();
      document.head.appendChild(s);
    } catch (eLoad) {}
  }

  function scheduleOffline() {
    var delay = 1500;
    if (document.readyState === "complete") setTimeout(loadOffline, delay);
    else
      window.addEventListener("load", function () {
        setTimeout(loadOffline, delay);
      });
  }
  scheduleOffline();
})();
