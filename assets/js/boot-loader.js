/**
 * MCD boot — short splash, never freeze mobile
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

  var seen = false;
  try {
    seen = sessionStorage.getItem("mcd_boot_seen") === "1";
  } catch (e2) {}

  var DUR = seen || isMobile ? 150 : 400;

  var css = document.createElement("style");
  css.textContent =
    "#boot-loader{position:fixed;inset:0;background:#050505;z-index:99999;display:flex;align-items:center;justify-content:center;transition:opacity .25s ease}" +
    "#boot-loader.hidden{opacity:0;pointer-events:none}" +
    "#boot-loader .boot-mark{color:#00e676;font:700 26px system-ui,sans-serif}";
  document.head.appendChild(css);

  var loader = document.createElement("div");
  loader.id = "boot-loader";
  loader.innerHTML = '<div class="boot-mark">MCD</div>';

  function finish() {
    try {
      sessionStorage.setItem("mcd_boot_seen", "1");
    } catch (e3) {}
    if (!loader || loader.classList.contains("hidden")) return;
    loader.classList.add("hidden");
    setTimeout(function () {
      if (loader.parentNode) loader.parentNode.removeChild(loader);
    }, 280);
  }

  function mount() {
    if (!document.body) {
      document.addEventListener("DOMContentLoaded", mount);
      return;
    }
    document.body.insertBefore(loader, document.body.firstChild);
    setTimeout(finish, DUR);
    setTimeout(finish, 800);
  }
  mount();

  function loadOffline() {
    if (window.__MCD_OFFLINE_SCRIPT__) return;
    window.__MCD_OFFLINE_SCRIPT__ = true;
    var s = document.createElement("script");
    s.async = true;
    s.defer = true;
    s.src = (function () {
      var scripts = document.getElementsByTagName("script");
      for (var i = 0; i < scripts.length; i++) {
        var src = scripts[i].src || "";
        if (src.indexOf("boot-loader.js") !== -1) {
          return src.replace(/boot-loader\.js.*$/, "offline-session.js");
        }
      }
      if ((location.pathname || "").indexOf("/programer") === 0) {
        return "/programer/assets/js/offline-session.js";
      }
      return "assets/js/offline-session.js";
    })();
    document.head.appendChild(s);
  }

  function schedule() {
    var delay = isMobile ? 5000 : 3000;
    if (document.readyState === "complete") setTimeout(loadOffline, delay);
    else
      window.addEventListener("load", function () {
        setTimeout(loadOffline, delay);
      });
  }
  schedule();
})();
