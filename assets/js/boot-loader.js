/**
 * MCD boot loader — lightweight, especially on mobile
 * Must never block the page for long (was causing black screen lag).
 */
(function () {
  if (window.__MCD_BOOT_DONE__) return;
  window.__MCD_BOOT_DONE__ = true;

  var isMobile = false;
  try {
    isMobile =
      window.matchMedia("(max-width:900px)").matches ||
      navigator.maxTouchPoints > 1 ||
      /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent || "");
  } catch (e) {}

  var tier = "high";
  try {
    var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (c) {
      if (c.saveData) tier = "low";
      else {
        var t = String(c.effectiveType || "").toLowerCase();
        if (t === "slow-2g" || t === "2g") tier = "low";
        else if (t === "3g") tier = "mid";
      }
    }
  } catch (e2) {}
  if (isMobile && tier === "high") tier = "mid";

  var FLAG = "mcd_boot_seen";
  var seen = false;
  try {
    seen = sessionStorage.getItem(FLAG) === "1";
  } catch (e3) {}

  /* Mobile / weak net: almost no splash. Desktop first visit: short only. */
  var DUR = 0;
  if (seen || tier === "low" || isMobile) {
    DUR = tier === "low" ? 120 : 220;
  } else if (tier === "mid") {
    DUR = 450;
  } else {
    DUR = 700;
  }

  var css = document.createElement("style");
  css.id = "boot-loader-css";
  css.textContent =
    "#boot-loader{position:fixed;inset:0;background:#050505;z-index:99999;display:flex;align-items:center;justify-content:center;transition:opacity .28s ease,visibility .28s}" +
    "#boot-loader.hidden{opacity:0;visibility:hidden;pointer-events:none}" +
    "#boot-loader .boot-mark{color:#00e676;font:700 28px/1 system-ui,sans-serif;letter-spacing:.06em;opacity:.9}";
  document.head.appendChild(css);

  var loader = document.createElement("div");
  loader.id = "boot-loader";
  loader.innerHTML = '<div class="boot-mark">MCD</div>';

  function finish() {
    try {
      sessionStorage.setItem(FLAG, "1");
    } catch (e4) {}
    if (!loader || loader.classList.contains("hidden")) return;
    loader.classList.add("hidden");
    setTimeout(function () {
      if (loader && loader.parentNode) loader.parentNode.removeChild(loader);
    }, 300);
  }

  function mount() {
    if (!document.body) {
      document.addEventListener("DOMContentLoaded", mount);
      return;
    }
    document.body.insertBefore(loader, document.body.firstChild);
    setTimeout(finish, DUR);
    /* hard safety: never stay black more than 1s */
    setTimeout(finish, 1000);
  }

  mount();

  /* Offline script: only AFTER page is usable — never compete with first paint */
  function loadOffline() {
    try {
      if (window.__MCD_OFFLINE_SCRIPT__) return;
      window.__MCD_OFFLINE_SCRIPT__ = true;
      var s = document.createElement("script");
      s.src = (function () {
        var scripts = document.getElementsByTagName("script");
        for (var i = 0; i < scripts.length; i++) {
          var src = scripts[i].src || "";
          if (src.indexOf("boot-loader.js") !== -1) {
            return src.replace(/boot-loader\.js.*$/, "offline-session.js");
          }
        }
        var p = location.pathname || "/";
        if (p.indexOf("/programer") === 0) return "/programer/assets/js/offline-session.js";
        return "assets/js/offline-session.js";
      })();
      s.defer = true;
      s.async = true;
      document.head.appendChild(s);
    } catch (e5) {}
  }

  function scheduleOffline() {
    var delay = isMobile ? 6000 : 3500;
    if (document.readyState === "complete") {
      setTimeout(loadOffline, delay);
    } else {
      window.addEventListener("load", function () {
        setTimeout(loadOffline, delay);
      });
    }
  }
  scheduleOffline();
})();
