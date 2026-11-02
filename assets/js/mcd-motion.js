/*! MCD adaptive performance — auto lighten by network, keep features */
(function () {
  if (window.__MCD_ADAPTIVE__) return;
  window.__MCD_ADAPTIVE__ = true;

  function detectTier() {
    var tier = "high";
    try {
      var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (c) {
        if (c.saveData) tier = "low";
        else {
          var t = String(c.effectiveType || "").toLowerCase();
          if (t === "slow-2g" || t === "2g") tier = "low";
          else if (t === "3g") tier = "mid";
          else if (t === "4g") tier = "high";
          // downlink in Mbps if available
          if (typeof c.downlink === "number") {
            if (c.downlink > 0 && c.downlink < 0.7) tier = "low";
            else if (c.downlink >= 0.7 && c.downlink < 2.5 && tier === "high") tier = "mid";
          }
          if (typeof c.rtt === "number") {
            if (c.rtt >= 800) tier = "low";
            else if (c.rtt >= 400 && tier === "high") tier = "mid";
          }
        }
      }
    } catch (e) {}
    // device memory hint (optional)
    try {
      if (navigator.deviceMemory && navigator.deviceMemory <= 2 && tier === "high") tier = "mid";
      if (navigator.deviceMemory && navigator.deviceMemory <= 1) tier = "low";
    } catch (e2) {}
    // hardware concurrency
    try {
      if (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2 && tier === "high") tier = "mid";
    } catch (e3) {}
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce && tier === "high") tier = "mid";
    return tier;
  }

  function applyTier(tier) {
    var b = document.body;
    if (!b) return;
    b.classList.remove("mcd-perf-high", "mcd-perf-mid", "mcd-perf-low");
    b.classList.add("mcd-perf-" + tier);
    b.setAttribute("data-mcd-perf", tier);
    window.__MCD_PERF_TIER__ = tier;
  }

  var tier = detectTier();

  function whenBody(fn) {
    if (document.body) fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  whenBody(function () { applyTier(tier); });

  // live adapt if network changes
  try {
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn && conn.addEventListener) {
      conn.addEventListener("change", function () {
        tier = detectTier();
        whenBody(function () { applyTier(tier); });
      });
    }
  } catch (e) {}

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function qs(s, n) { return Array.prototype.slice.call((n || document).querySelectorAll(s)); }

  function addLiveChip() {
    if (tier === "low") return; // skip extra DOM on low
    var header = document.querySelector("header");
    if (!header || header.querySelector(".mcd-live-chip")) return;
    var chip = document.createElement("span");
    chip.className = "mcd-live-chip";
    chip.innerHTML = '<span class="dot" aria-hidden="true"></span><span>SYSTEM ONLINE</span>';
    var logo = header.querySelector(".logo");
    if (logo) logo.insertAdjacentElement("afterend", chip);
    else header.appendChild(chip);
  }

  function setupHeader() {
    var h = document.querySelector("header");
    if (!h) return;
    var ticking = false;
    function upd() {
      ticking = false;
      if (window.scrollY > 6) h.classList.add("mcd-scrolled");
      else h.classList.remove("mcd-scrolled");
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(upd); }
    }, { passive: true });
    upd();
  }

  function setupReveal() {
    if (reduce || tier === "low") return;
    var max = tier === "mid" ? 14 : 28;
    var targets = qs("main .home-section, main .card, main .lang, main .lang-link, main .example-unit, main article.card").slice(0, max);
    if (!targets.length) return;
    targets.forEach(function (el) { el.classList.add("mcd-reveal"); });
    if (!("IntersectionObserver" in window)) {
      targets.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].isIntersecting) {
          entries[i].target.classList.add("is-in");
          io.unobserve(entries[i].target);
        }
      }
    }, { threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  }

  function setupRipple() {
    if (reduce || tier === "low") return;
    document.addEventListener("click", function (e) {
      var el = e.target.closest("a.lang, a.lang-link, .trybtn, button, .start-card, nav a, .navbtn a, .side a, .btn-pin");
      if (!el) return;
      var r = document.createElement("span");
      r.className = "mcd-ripple-span";
      var rect = el.getBoundingClientRect();
      r.style.left = ((e.clientX || rect.left + rect.width / 2) - rect.left) + "px";
      r.style.top = ((e.clientY || rect.top + rect.height / 2) - rect.top) + "px";
      el.classList.add("mcd-rippling");
      el.appendChild(r);
      setTimeout(function () { if (r.parentNode) r.parentNode.removeChild(r); }, 400);
    }, { passive: true });
  }

  function setupHeroMatrix() {
    if (reduce || tier === "low") return;
    var hero = document.querySelector(".hero");
    if (!hero) return;
    var path = (location.pathname || "").replace(/\\/g, "/");
    var depth = path.split("/").filter(Boolean).length;
    if (depth > 2) return;
    if (!(/\/$/.test(path) || /index\.html?$/i.test(path))) return;

    var canvas = document.getElementById("mcd-algo-canvas");
    if (!canvas) {
      canvas = document.createElement("canvas");
      canvas.id = "mcd-algo-canvas";
      canvas.setAttribute("aria-hidden", "true");
      hero.insertBefore(canvas, hero.firstChild);
    }
    var ctx = canvas.getContext("2d");
    if (!ctx) return;
    var chars = "01{}[]MCD";
    var cols = [];
    var running = true;
    var last = 0;
    var fpsGap = tier === "mid" ? 80 : 55;

    function resize() {
      var r = hero.getBoundingClientRect();
      canvas.width = Math.max(1, r.width | 0);
      canvas.height = Math.max(1, r.height | 0);
      canvas.style.width = r.width + "px";
      canvas.style.height = r.height + "px";
      var gap = tier === "mid" ? 34 : 26;
      var n = Math.max(5, Math.min(tier === "mid" ? 14 : 22, Math.floor(r.width / gap)));
      cols = [];
      for (var i = 0; i < n; i++) cols.push({ x: i * gap + 6, y: Math.random() * r.height, s: 0.5 + Math.random() * 0.7 });
    }
    function frame(ts) {
      if (!running) return;
      if (window.__MCD_PERF_TIER__ === "low") { running = false; return; }
      if (ts - last < fpsGap) { requestAnimationFrame(frame); return; }
      last = ts;
      var r = hero.getBoundingClientRect();
      ctx.fillStyle = "rgba(2,8,5,0.22)";
      ctx.fillRect(0, 0, r.width, r.height);
      ctx.font = "11px monospace";
      ctx.fillStyle = "rgba(0,230,118,0.42)";
      for (var i = 0; i < cols.length; i++) {
        var c = cols[i];
        ctx.fillText(chars[(Math.random() * chars.length) | 0], c.x, c.y);
        c.y += c.s * 9;
        if (c.y > r.height + 16) { c.y = -16; c.s = 0.5 + Math.random() * 0.7; }
      }
      requestAnimationFrame(frame);
    }
    resize();
    window.addEventListener("resize", resize, { passive: true });
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) running = false;
      else if (window.__MCD_PERF_TIER__ !== "low") { running = true; last = 0; requestAnimationFrame(frame); }
    });
    requestAnimationFrame(frame);
  }

  function setupBinaryWind() {
    if (reduce) return;
    // low tier: skip wind entirely
    if (tier === "low") return;
    var host = document.getElementById("mcd-binary-wind");
    if (!host) {
      host = document.createElement("div");
      host.id = "mcd-binary-wind";
      host.setAttribute("aria-hidden", "true");
      document.body.appendChild(host);
    }
    var fragments = ["ERR_0x7F01","0xDEAD::01","NULL<<01","01??01","bitflip=1","###CORRUPT","MCD//ok"];
    function randBin(n) {
      var s = "";
      for (var i = 0; i < n; i++) s += (Math.random() > 0.5 ? "1" : "0");
      return s;
    }
    function blow() {
      if (document.hidden) return;
      if (window.__MCD_PERF_TIER__ === "low") return;
      var cur = window.__MCD_PERF_TIER__ || tier;
      host.innerHTML = "";
      host.classList.add("is-blowing");
      var wash = document.createElement("div");
      wash.className = "wash";
      host.appendChild(wash);
      if (cur !== "mid") {
        for (var t = 0; t < 2; t++) {
          var tear = document.createElement("div");
          tear.className = "tear";
          tear.style.top = (15 + Math.random() * 70) + "vh";
          host.appendChild(tear);
        }
      }
      var isMobile = window.matchMedia && window.matchMedia("(max-width:700px)").matches;
      var count = cur === "mid" ? (isMobile ? 10 : 16) : (isMobile ? 18 : 28);
      var frag = document.createDocumentFragment();
      for (var i = 0; i < count; i++) {
        var bit = document.createElement("span");
        bit.className = "bit";
        if (Math.random() < 0.15) bit.className += " err";
        bit.textContent = Math.random() < 0.3 ? fragments[(Math.random() * fragments.length) | 0] : randBin(8 + ((Math.random() * 12) | 0));
        bit.style.top = (Math.random() * 94) + "vh";
        bit.style.left = (-18 - Math.random() * 18) + "vw";
        bit.style.fontSize = (10 + Math.random() * 7) + "px";
        bit.style.animationDuration = (2 + Math.random() * 1.2) + "s";
        bit.style.animationDelay = (Math.random() * 0.35) + "s";
        frag.appendChild(bit);
      }
      host.appendChild(frag);
      setTimeout(function () { host.classList.remove("is-blowing"); host.innerHTML = ""; }, 2600);
    }
    setTimeout(blow, 9000);
    setInterval(function () { if (!document.hidden) blow(); }, 60000);
  }

  function boot() {
    document.body.classList.add("mcd-ready");
    applyTier(tier);
    addLiveChip();
    setupHeader();
    setupReveal();
    setupRipple();
    setupHeroMatrix();
    setupBinaryWind();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
