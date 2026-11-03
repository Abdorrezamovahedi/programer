/*! MCD adaptive performance — device power + network, zero lag on weak hardware */
(function () {
  if (window.__MCD_ADAPTIVE__) return;
  window.__MCD_ADAPTIVE__ = true;

  function scoreDevice() {
    var score = 70; // start neutral-high

    try {
      var cores = navigator.hardwareConcurrency || 4;
      if (cores <= 2) score -= 30;
      else if (cores <= 4) score -= 12;
      else if (cores >= 8) score += 8;
    } catch (e) {}

    try {
      var mem = navigator.deviceMemory; // GiB, Chrome/Android mainly
      if (typeof mem === 'number') {
        if (mem <= 1) score -= 35;
        else if (mem <= 2) score -= 22;
        else if (mem <= 4) score -= 8;
        else if (mem >= 8) score += 6;
      }
    } catch (e2) {}

    try {
      var ua = String(navigator.userAgent || '').toLowerCase();
      var mobile = /android|iphone|ipod|mobile|windows phone/.test(ua);
      var tablet = /ipad|tablet/.test(ua);
      if (mobile) score -= 15;
      if (tablet) score -= 6;
      if (/android [2-6]\./.test(ua)) score -= 20;
    } catch (e3) {}

    try {
      if (navigator.maxTouchPoints > 1 && window.innerWidth < 900) score -= 8;
    } catch (e4) {}

    try {
      var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (c) {
        if (c.saveData) score -= 25;
        var t = String(c.effectiveType || '').toLowerCase();
        if (t === 'slow-2g' || t === '2g') score -= 35;
        else if (t === '3g') score -= 18;
        if (typeof c.downlink === 'number') {
          if (c.downlink > 0 && c.downlink < 0.6) score -= 30;
          else if (c.downlink < 1.5) score -= 12;
        }
        if (typeof c.rtt === 'number') {
          if (c.rtt >= 700) score -= 25;
          else if (c.rtt >= 350) score -= 10;
        }
      }
    } catch (e5) {}

    try {
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        score -= 40;
      }
    } catch (e6) {}

    try {
      if (navigator.getBattery) {
        // async; handled later
      }
    } catch (e7) {}

    return score;
  }

  function tierFromScore(score) {
    if (score < 35) return 'low';
    if (score < 58) return 'mid';
    return 'high';
  }

  function applyTier(tier) {
    var b = document.body;
    if (!b) return;
    b.classList.remove('mcd-perf-high', 'mcd-perf-mid', 'mcd-perf-low');
    b.classList.add('mcd-perf-' + tier);
    b.setAttribute('data-mcd-perf', tier);
    window.__MCD_PERF_TIER__ = tier;

    // Inject CSS limits once
    if (!document.getElementById('mcd-perf-css')) {
      var st = document.createElement('style');
      st.id = 'mcd-perf-css';
      st.textContent =
        'body.mcd-perf-low *{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}' +
        'body.mcd-perf-low #mcd-algo-canvas,body.mcd-perf-low #mcd-binary-wind,body.mcd-perf-low .mcd-live-chip{display:none!important}' +
        'body.mcd-perf-low .mcd-reveal{opacity:1!important;transform:none!important}' +
        'body.mcd-perf-mid #mcd-binary-wind .bit{animation-duration:2.4s!important}' +
        'body.mcd-perf-mid #mcd-algo-canvas{opacity:.35!important}' +
        'body.mcd-perf-low .line-exp,body.mcd-perf-mid .line-exp{animation:none!important}';
      document.head.appendChild(st);
    }
  }

  var score = scoreDevice();
  var tier = tierFromScore(score);
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function whenBody(fn) {
    if (document.body) fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
  whenBody(function () { applyTier(tier); });

  // Battery: if discharging and low, drop tier
  try {
    if (navigator.getBattery) {
      navigator.getBattery().then(function (bat) {
        function checkBat() {
          if (bat.dischargingTime !== Infinity && bat.level > 0 && bat.level < 0.15 && !bat.charging) {
            if (tier !== 'low') {
              tier = 'low';
              whenBody(function () { applyTier(tier); });
            }
          }
        }
        checkBat();
        bat.addEventListener('levelchange', checkBat);
        bat.addEventListener('chargingchange', checkBat);
      }).catch(function () {});
    }
  } catch (eb) {}

  // Live network change
  try {
    var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn && conn.addEventListener) {
      conn.addEventListener('change', function () {
        score = scoreDevice();
        tier = tierFromScore(score);
        whenBody(function () { applyTier(tier); });
      });
    }
  } catch (e) {}

  // FPS probe: if device janks, auto-downgrade once
  function probeFps() {
    if (tier === 'low') return;
    var frames = 0;
    var start = 0;
    function tick(ts) {
      if (!start) start = ts;
      frames++;
      if (ts - start < 1000) {
        requestAnimationFrame(tick);
        return;
      }
      var fps = frames;
      if (fps < 28 && tier === 'high') {
        tier = 'mid';
        whenBody(function () { applyTier(tier); });
      } else if (fps < 18) {
        tier = 'low';
        whenBody(function () { applyTier(tier); });
      }
    }
    try { requestAnimationFrame(tick); } catch (e) {}
  }
  setTimeout(probeFps, 1200);

  function qs(s, n) {
    return Array.prototype.slice.call((n || document).querySelectorAll(s));
  }

  function addLiveChip() {
    if (tier === 'low') return;
    var header = document.querySelector('header');
    if (!header || header.querySelector('.mcd-live-chip')) return;
    var chip = document.createElement('span');
    chip.className = 'mcd-live-chip';
    chip.innerHTML = '<span class="dot" aria-hidden="true"></span><span>SYSTEM ONLINE</span>';
    var logo = header.querySelector('.logo');
    if (logo) logo.insertAdjacentElement('afterend', chip);
    else header.appendChild(chip);
  }

  function setupHeader() {
    var h = document.querySelector('header');
    if (!h) return;
    var ticking = false;
    function upd() {
      ticking = false;
      if (window.scrollY > 6) h.classList.add('mcd-scrolled');
      else h.classList.remove('mcd-scrolled');
    }
    window.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(upd);
      }
    }, { passive: true });
    upd();
  }

  function setupReveal() {
    if (reduce || tier === 'low') return;
    var max = tier === 'mid' ? 10 : 24;
    var targets = qs('main .home-section, main .card, main .lang, main .lang-link, main .example-unit, main article.card').slice(0, max);
    if (!targets.length) return;
    targets.forEach(function (el) { el.classList.add('mcd-reveal'); });
    if (!('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].isIntersecting) {
          entries[i].target.classList.add('is-in');
          io.unobserve(entries[i].target);
        }
      }
    }, { threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  }

  function setupRipple() {
    if (reduce || tier === 'low') return;
    document.addEventListener('click', function (e) {
      var el = e.target.closest('a.lang, a.lang-link, .trybtn, button, .start-card, nav a, .navbtn a, .side a, .btn-pin');
      if (!el) return;
      var r = document.createElement('span');
      r.className = 'mcd-ripple-span';
      var rect = el.getBoundingClientRect();
      r.style.left = ((e.clientX || rect.left + rect.width / 2) - rect.left) + 'px';
      r.style.top = ((e.clientY || rect.top + rect.height / 2) - rect.top) + 'px';
      el.classList.add('mcd-rippling');
      el.appendChild(r);
      setTimeout(function () { if (r.parentNode) r.parentNode.removeChild(r); }, 380);
    }, { passive: true });
  }

  function setupHeroMatrix() {
    if (reduce || tier === 'low') return;
    var hero = document.querySelector('.hero');
    if (!hero) return;
    var path = (location.pathname || '').replace(/\\/g, '/');
    var depth = path.split('/').filter(Boolean).length;
    if (depth > 2) return;
    if (!(/\/$/.test(path) || /index\.html?$/i.test(path))) return;

    var canvas = document.getElementById('mcd-algo-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'mcd-algo-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      hero.insertBefore(canvas, hero.firstChild);
    }
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    var chars = '01{}[]MCD';
    var cols = [];
    var running = true;
    var last = 0;
    var fpsGap = tier === 'mid' ? 90 : 55;

    function resize() {
      var r = hero.getBoundingClientRect();
      canvas.width = Math.max(1, r.width | 0);
      canvas.height = Math.max(1, r.height | 0);
      canvas.style.width = r.width + 'px';
      canvas.style.height = r.height + 'px';
      var gap = tier === 'mid' ? 36 : 26;
      var n = Math.max(4, Math.min(tier === 'mid' ? 12 : 20, Math.floor(r.width / gap)));
      cols = [];
      for (var i = 0; i < n; i++) cols.push({ x: i * gap + 6, y: Math.random() * r.height, s: 0.5 + Math.random() * 0.7 });
    }
    function frame(ts) {
      if (!running) return;
      if (window.__MCD_PERF_TIER__ === 'low') { running = false; return; }
      if (ts - last < fpsGap) { requestAnimationFrame(frame); return; }
      last = ts;
      var r = hero.getBoundingClientRect();
      ctx.fillStyle = 'rgba(2,8,5,0.22)';
      ctx.fillRect(0, 0, r.width, r.height);
      ctx.font = '11px monospace';
      ctx.fillStyle = 'rgba(0,230,118,0.42)';
      for (var i = 0; i < cols.length; i++) {
        var c = cols[i];
        ctx.fillText(chars[(Math.random() * chars.length) | 0], c.x, c.y);
        c.y += c.s * 9;
        if (c.y > r.height + 16) { c.y = -16; c.s = 0.5 + Math.random() * 0.7; }
      }
      requestAnimationFrame(frame);
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) running = false;
      else if (window.__MCD_PERF_TIER__ !== 'low') {
        running = true;
        last = 0;
        requestAnimationFrame(frame);
      }
    });
    requestAnimationFrame(frame);
  }

  function setupBinaryWind() {
    if (reduce || tier === 'low') return;
    var host = document.getElementById('mcd-binary-wind');
    if (!host) {
      host = document.createElement('div');
      host.id = 'mcd-binary-wind';
      host.setAttribute('aria-hidden', 'true');
      document.body.appendChild(host);
    }
    var fragments = ['ERR_0x7F01', '0xDEAD::01', 'NULL<<01', '01??01', 'bitflip=1', '###CORRUPT', 'MCD//ok'];
    function randBin(n) {
      var s = '';
      for (var i = 0; i < n; i++) s += Math.random() > 0.5 ? '1' : '0';
      return s;
    }
    function blow() {
      if (document.hidden) return;
      if (window.__MCD_PERF_TIER__ === 'low') return;
      var cur = window.__MCD_PERF_TIER__ || tier;
      host.innerHTML = '';
      host.classList.add('is-blowing');
      var wash = document.createElement('div');
      wash.className = 'wash';
      host.appendChild(wash);
      if (cur !== 'mid') {
        for (var t = 0; t < 2; t++) {
          var tear = document.createElement('div');
          tear.className = 'tear';
          tear.style.top = 15 + Math.random() * 70 + 'vh';
          host.appendChild(tear);
        }
      }
      var isMobile = window.matchMedia && window.matchMedia('(max-width:700px)').matches;
      var count = cur === 'mid' ? (isMobile ? 8 : 14) : isMobile ? 16 : 26;
      var frag = document.createDocumentFragment();
      for (var i = 0; i < count; i++) {
        var bit = document.createElement('span');
        bit.className = 'bit' + (Math.random() < 0.15 ? ' err' : '');
        bit.textContent = Math.random() < 0.3 ? fragments[(Math.random() * fragments.length) | 0] : randBin(8 + ((Math.random() * 10) | 0));
        bit.style.top = Math.random() * 94 + 'vh';
        bit.style.left = -18 - Math.random() * 18 + 'vw';
        bit.style.fontSize = 10 + Math.random() * 7 + 'px';
        bit.style.animationDuration = 2 + Math.random() * 1.1 + 's';
        bit.style.animationDelay = Math.random() * 0.3 + 's';
        frag.appendChild(bit);
      }
      host.appendChild(frag);
      setTimeout(function () {
        host.classList.remove('is-blowing');
        host.innerHTML = '';
      }, 2500);
    }
    setTimeout(blow, tier === 'mid' ? 14000 : 9000);
    setInterval(function () {
      if (!document.hidden && window.__MCD_PERF_TIER__ !== 'low') blow();
    }, tier === 'mid' ? 90000 : 60000);
  }

  function boot() {
    document.body.classList.add('mcd-ready');
    applyTier(tier);
    setupHeader();
    if (tier === 'low') return; // pure content path — no lag effects
    addLiveChip();
    setupReveal();
    setupRipple();
    setupHeroMatrix();
    setupBinaryWind();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
