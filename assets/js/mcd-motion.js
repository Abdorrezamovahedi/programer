/*! MCD motion — page transitions + code terminal feel */
(function () {
  if (window.__MCD_MOTION__) return;
  window.__MCD_MOTION__ = true;

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function ready() {
    document.body.classList.add("mcd-ready");

    // Hero class on homepage
    var hero = document.querySelector(".hero");
    if (hero && (location.pathname.endsWith("/") || /index\.html?$/.test(location.pathname) || location.pathname.split("/").filter(Boolean).length <= 1)) {
      // only enhance main-looking heroes
      if (!hero.classList.contains("mcd-hero")) hero.classList.add("mcd-hero");
    }

    // Mark code blocks
    document.querySelectorAll("pre").forEach(function (pre) {
      pre.classList.add("mcd-terminal");
      // avoid double header if already inside codewrap with ::before
      if (pre.parentElement && pre.parentElement.classList.contains("codewrap")) {
        pre.classList.remove("mcd-terminal");
      }
    });

    if (reduce) return;

    // Page transition overlay
    var fx = document.getElementById("mcd-page-fx");
    if (!fx) {
      fx = document.createElement("div");
      fx.id = "mcd-page-fx";
      fx.innerHTML = '<div class="fx-line" aria-hidden="true"></div>';
      document.body.appendChild(fx);
    }

    document.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      if (!a) return;
      var href = a.getAttribute("href");
      if (!href || href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("javascript:")) return;
      if (a.target === "_blank" || a.hasAttribute("download")) return;
      // external
      if (/^https?:/i.test(href) && href.indexOf(location.host) === -1) return;
      // same page hash-only already returned
      e.preventDefault();
      fx.classList.add("is-on");
      window.setTimeout(function () {
        location.href = a.href;
      }, 220);
    }, true);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ready);
  } else {
    ready();
  }
})();
