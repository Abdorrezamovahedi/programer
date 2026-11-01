/*! MCD Algo Atmosphere — light programming vibe */
(function () {
  if (window.__MCD_ALGO_ATMO__) return;
  window.__MCD_ALGO_ATMO__ = true;

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function qs(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }

  function addLiveChip() {
    var header = document.querySelector("header");
    if (!header || header.querySelector(".mcd-live-chip")) return;
    var chip = document.createElement("span");
    chip.className = "mcd-live-chip";
    chip.innerHTML = '<span class="dot" aria-hidden="true"></span><span>SYSTEM ONLINE</span>';
    // place near logo if possible
    var logo = header.querySelector(".logo");
    if (logo && logo.parentNode === header) {
      logo.insertAdjacentElement("afterend", chip);
    } else {
      header.appendChild(chip);
    }
  }

  function setupHeaderScroll() {
    var h = document.querySelector("header");
    if (!h) return;
    var ticking = false;
    function update() {
      ticking = false;
      if (window.scrollY > 6) h.classList.add("mcd-scrolled");
      else h.classList.remove("mcd-scrolled");
    }
    window.addEventListener("scroll", function () {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    }, { passive: true });
    update();
  }

  function setupReveal() {
    var targets = qs("main .home-section, main .card, main .lang, main .lang-link, main .example-unit, main article.card").slice(0, 36);
    if (!targets.length) return;
    if (reduce) {
      targets.forEach(function (el) { el.classList.add("mcd-reveal", "is-in"); });
      return;
    }
    targets.forEach(function (el) { el.classList.add("mcd-reveal"); });
    if (!("IntersectionObserver" in window)) {
      targets.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("is-in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  }

  function setupRipple() {
    if (reduce) return;
    document.addEventListener("click", function (e) {
      var el = e.target.closest("a.lang, a.lang-link, .trybtn, button, .start-card, nav a, .navbtn a, .side a, .btn-pin");
      if (!el) return;
      el.classList.add("mcd-rippling");
      var r = document.createElement("span");
      r.className = "mcd-ripple-span";
      var rect = el.getBoundingClientRect();
      r.style.left = ((e.clientX || rect.left + rect.width / 2) - rect.left) + "px";
      r.style.top = ((e.clientY || rect.top + rect.height / 2) - rect.top) + "px";
      el.appendChild(r);
      setTimeout(function () { if (r.parentNode) r.parentNode.removeChild(r); }, 480);
    }, { passive: true });
  }

  // Lightweight matrix only on homepage hero (not whole site)
  function setupHeroMatrix() {
    if (reduce) return;
    var hero = document.querySelector(".hero");
    if (!hero) return;
    // only main home-ish pages
    var path = (location.pathname || "").replace(/\\/g, "/");
    var isHome = /\/$/.test(path) || /index\.html?$/i.test(path);
    if (!isHome) return;
    if (path.split("/").filter(Boolean).length > 2) return;

    var canvas = document.getElementById("mcd-algo-canvas");
    if (!canvas) {
      canvas = document.createElement("canvas");
      canvas.id = "mcd-algo-canvas";
      canvas.setAttribute("aria-hidden", "true");
      hero.insertBefore(canvas, hero.firstChild);
    }
    var ctx = canvas.getContext("2d");
    if (!ctx) return;
    var chars = "01{}[]<>/=+*#MCD";
    var cols = [];
    var running = true;
    var last = 0;

    function resize() {
      var r = hero.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      canvas.width = Math.max(1, (r.width * dpr) | 0);
      canvas.height = Math.max(1, (r.height * dpr) | 0);
      canvas.style.width = r.width + "px";
      canvas.style.height = r.height + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var w = r.width;
      var font = 12;
      var n = Math.max(8, Math.floor(w / 18));
      cols = [];
      for (var i = 0; i < n; i++) {
        cols.push({ x: i * 18 + 4, y: Math.random() * r.height, s: 0.6 + Math.random() * 0.9 });
      }
    }

    function frame(ts) {
      if (!running) return;
      if (ts - last < 50) { // ~20fps max — low lag
        requestAnimationFrame(frame);
        return;
      }
      last = ts;
      var r = hero.getBoundingClientRect();
      ctx.fillStyle = "rgba(2,8,5,0.18)";
      ctx.fillRect(0, 0, r.width, r.height);
      ctx.font = "12px monospace";
      ctx.fillStyle = "rgba(0,230,118,0.55)";
      for (var i = 0; i < cols.length; i++) {
        var c = cols[i];
        var ch = chars[(Math.random() * chars.length) | 0];
        ctx.fillText(ch, c.x, c.y);
        c.y += c.s * 10;
        if (c.y > r.height + 20) {
          c.y = -20;
          c.s = 0.6 + Math.random() * 0.9;
        }
      }
      requestAnimationFrame(frame);
    }

    resize();
    window.addEventListener("resize", resize, { passive: true });
    // Pause when tab hidden
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) running = false;
      else { running = true; last = 0; requestAnimationFrame(frame); }
    });
    requestAnimationFrame(frame);
  }

  function markTerminals() {
    var list = qs("pre");
    for (var i = 0; i < list.length && i < 24; i++) {
      var pre = list[i];
      if (pre.closest(".codewrap") || pre.id === "edCode") pre.classList.remove("mcd-terminal");
      else pre.classList.add("mcd-terminal");
    }
  }

  
  function beautifyCodeBlocks() {
    var wraps = document.querySelectorAll(".codewrap");
    var max = Math.min(wraps.length, 40);
    for (var i = 0; i < max; i++) {
      var w = wraps[i];
      if (!w.querySelector(".mcd-code-status")) {
        var st = document.createElement("div");
        st.className = "mcd-code-status";
        st.innerHTML = '<span class="mcd-code-bars"><i></i><i></i><i></i><i></i></span><span>process</span>';
        w.appendChild(st);
      }
    }
  }

  
  function setupBinaryWind() {
    if (reduce) return;
    var host = document.getElementById("mcd-binary-wind");
    if (!host) {
      host = document.createElement("div");
      host.id = "mcd-binary-wind";
      host.setAttribute("aria-hidden", "true");
      document.body.appendChild(host);
    }

    var fragments = [
      "01001101 01000011 01000100",
      "ERR_0x7F01",
      "0xDEAD::01",
      "NULL<<01",
      "segfault@0x01",
      "///broken_stream",
      "01??01??00",
      "core.dmp",
      "stack:0x0",
      ">>> FAIL",
      "0|1|0|1|X",
      "sync_lost",
      "###CORRUPT",
      "bitflip=1",
      "01 00 01 ~~",
      "MCD//rebooting",
      "overload...",
      "0x00FF00",
      "timeout=1",
      "///"
    ];

    function randBin(n) {
      var s = "";
      for (var i = 0; i < n; i++) {
        if (Math.random() < 0.08) s += ["?", "#", "X", "~", "/"][(Math.random() * 5) | 0];
        else s += (Math.random() > 0.5 ? "1" : "0");
        if (Math.random() < 0.12) s += " ";
      }
      return s;
    }

    function blow() {
      if (document.hidden) return;
      host.innerHTML = "";
      host.classList.add("is-blowing");

      var wash = document.createElement("div");
      wash.className = "wash";
      host.appendChild(wash);

      // 2-3 tear lines
      for (var t = 0; t < 3; t++) {
        var tear = document.createElement("div");
        tear.className = "tear";
        tear.style.top = (12 + Math.random() * 76) + "vh";
        tear.style.animationDelay = (Math.random() * 0.25) + "s";
        host.appendChild(tear);
      }

      var isMobile = window.matchMedia && window.matchMedia("(max-width: 700px)").matches;
      var count = isMobile ? 22 : 42;
      var frag = document.createDocumentFragment();

      for (var i = 0; i < count; i++) {
        var bit = document.createElement("span");
        bit.className = "bit";
        var roll = Math.random();
        if (roll < 0.18) bit.className += " err";
        else if (roll < 0.3) bit.className += " warn";
        else if (roll < 0.4) bit.className += " ghost";

        if (Math.random() < 0.35) {
          bit.textContent = fragments[(Math.random() * fragments.length) | 0];
        } else {
          bit.textContent = randBin(8 + ((Math.random() * 18) | 0));
        }

        bit.style.top = (Math.random() * 94) + "vh";
        bit.style.left = (-18 - Math.random() * 25) + "vw";
        bit.style.fontSize = (10 + Math.random() * 9) + "px";
        var dur = 1.8 + Math.random() * 1.5;
        bit.style.animationDuration = dur + "s";
        bit.style.animationDelay = (Math.random() * 0.55) + "s";
        frag.appendChild(bit);
      }
      host.appendChild(frag);

      setTimeout(function () {
        host.classList.remove("is-blowing");
        host.innerHTML = "";
      }, 3000);
    }

    setTimeout(blow, 8000);
    setInterval(blow, 60000);
  }

  function boot() {
    document.body.classList.add("mcd-ready");
    addLiveChip();
    setupHeaderScroll();
    setupReveal();
    setupRipple();
    markTerminals();
    beautifyCodeBlocks();
    setupHeroMatrix();
    setupBinaryWind();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
