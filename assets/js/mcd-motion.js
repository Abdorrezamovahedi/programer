/*! MCD adaptive performance — stable tier, lag-safe, non-intrusive */
(function () {
  if (window.__MCD_ADAPTIVE__) return;
  window.__MCD_ADAPTIVE__ = true;

  var TIER_KEY = 'mcd_perf_tier_v2';

  function isMobileLike() {
    try {
      var ua = String(navigator.userAgent || '').toLowerCase();
      if (/android|iphone|ipod|mobile|windows phone|ipad|tablet/.test(ua)) return true;
      if (navigator.maxTouchPoints > 1 && window.innerWidth < 900) return true;
    } catch (e) {}
    return false;
  }

  function scoreDevice() {
    var score = 62;
    try {
      var cores = navigator.hardwareConcurrency || 4;
      if (cores <= 2) score -= 28;
      else if (cores <= 4) score -= 10;
      else if (cores >= 8) score += 6;
    } catch (e) {}
    try {
      var mem = navigator.deviceMemory;
      if (typeof mem === 'number') {
        if (mem <= 1) score -= 30;
        else if (mem <= 2) score -= 18;
        else if (mem <= 4) score -= 6;
      }
    } catch (e2) {}
    if (isMobileLike()) score -= 14;
    try {
      var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (c) {
        if (c.saveData) score -= 20;
        var t = String(c.effectiveType || '').toLowerCase();
        if (t === 'slow-2g' || t === '2g') score -= 28;
        else if (t === '3g') score -= 14;
        if (typeof c.downlink === 'number' && c.downlink > 0 && c.downlink < 1) score -= 16;
        if (typeof c.rtt === 'number' && c.rtt >= 500) score -= 12;
      }
    } catch (e3) {}
    try {
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) score -= 35;
    } catch (e4) {}
    return score;
  }

  function tierFromScore(score) {
    if (score < 38) return 'low';
    if (score < 68) return 'mid';
    return 'high';
  }

  function rank(t) {
    return t === 'high' ? 3 : t === 'mid' ? 2 : 1;
  }

  function readCachedTier() {
    try {
      var t = sessionStorage.getItem(TIER_KEY);
      if (t === 'low' || t === 'mid' || t === 'high') return t;
    } catch (e) {}
    return null;
  }

  function writeCachedTier(t) {
    try { sessionStorage.setItem(TIER_KEY, t); } catch (e) {}
  }

  var computed = tierFromScore(scoreDevice());
  var cached = readCachedTier();
  var tier = cached || computed;
  if (cached && rank(computed) < rank(cached)) tier = computed;
  if (isMobileLike() && tier === 'high') tier = 'mid';
  writeCachedTier(tier);

  var reduce = false;
  try {
    reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  } catch (e5) {}
  if (reduce) tier = 'low';

  function applyTier(t) {
    var b = document.body;
    if (!b) return;
    b.classList.remove('mcd-perf-high', 'mcd-perf-mid', 'mcd-perf-low');
    b.classList.add('mcd-perf-' + t);
    window.__MCD_PERF_TIER__ = t;
    writeCachedTier(t);
    if (!document.getElementById('mcd-perf-style')) {
      var s = document.createElement('style');
      s.id = 'mcd-perf-style';
      s.textContent =
        'body.mcd-perf-low #mcd-algo-canvas,body.mcd-perf-low #mcd-binary-wind,body.mcd-perf-low .mcd-live-chip{display:none!important}' +
        'body.mcd-perf-low .mcd-reveal{opacity:1!important;transform:none!important;transition:none!important}' +
        'body.mcd-perf-mid #mcd-algo-canvas,body.mcd-perf-mid #mcd-binary-wind{display:none!important}' +
        'body.mcd-perf-low .mcd-ripple-span{display:none!important}' +
        '#mcd-binary-wind{pointer-events:none;opacity:0.35}' +
        '#mcd-algo-canvas{opacity:0.35;pointer-events:none}';
      document.head.appendChild(s);
    }
  }

  function whenBody(fn) {
    if (document.body) fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }
  whenBody(function () { applyTier(tier); });

  function downgrade(to) {
    if (rank(to) >= rank(tier)) return;
    tier = to;
    whenBody(function () { applyTier(tier); });
    window.__MCD_PERF_TIER__ = tier;
  }

  setTimeout(function () {
    try {
      var next = tierFromScore(scoreDevice());
      if (rank(next) < rank(tier)) downgrade(next);
    } catch (e) {}
  }, 2500);

  setTimeout(function () {
    if (tier === 'low' || document.hidden) return;
    var frames = 0, start = performance.now();
    function tick(now) {
      frames++;
      if (now - start < 1000) {
        requestAnimationFrame(tick);
        return;
      }
      var fps = frames;
      if (fps < 22) downgrade('low');
      else if (fps < 40 && tier === 'high') downgrade('mid');
    }
    try { requestAnimationFrame(tick); } catch (e) {}
  }, 1800);

  function qs(s, n) {
    return Array.prototype.slice.call((n || document).querySelectorAll(s));
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
    var max = tier === 'mid' ? 5 : 10;
    var targets = qs('main .home-section, main .card, main .lang, main .lang-link, main article.card').slice(0, max);
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
    }, { threshold: 0.1 });
    targets.forEach(function (el) { io.observe(el); });
  }

  function setupRipple() {
    if (reduce || tier !== 'high') return;
    document.addEventListener('click', function (e) {
      if (window.__MCD_PERF_TIER__ !== 'high') return;
      var el = e.target.closest('a.lang, a.lang-link, .trybtn, .start-card, nav a');
      if (!el) return;
      var r = document.createElement('span');
      r.className = 'mcd-ripple-span';
      var rect = el.getBoundingClientRect();
      r.style.left = (e.clientX - rect.left) + 'px';
      r.style.top = (e.clientY - rect.top) + 'px';
      el.appendChild(r);
      setTimeout(function () { if (r.parentNode) r.parentNode.removeChild(r); }, 350);
    }, { passive: true });
  }

  function setupHeroMatrix() {
    if (reduce || tier !== 'high' || isMobileLike()) return;
    var hero = document.querySelector('.hero');
    if (!hero) return;
    var path = (location.pathname || '').replace(/\\/g, '/');
    if (!(/\/$/.test(path) || /index\.html?$/i.test(path))) return;
    if (path.split('/').filter(Boolean).length > 2) return;
    var canvas = document.getElementById('mcd-algo-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'mcd-algo-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      hero.style.position = hero.style.position || 'relative';
      hero.appendChild(canvas);
    }
    var ctx = canvas.getContext('2d');
    if (!ctx) return;
    var cols = [];
    var chars = '01';
    var running = true;
    var last = 0;
    var gapMs = 80;
    function resize() {
      var r = hero.getBoundingClientRect();
      canvas.width = Math.max(1, r.width | 0);
      canvas.height = Math.max(1, r.height | 0);
      canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:0.35;z-index:0';
      cols = [];
      var n = Math.max(6, (r.width / 28) | 0);
      for (var i = 0; i < n; i++) cols.push({ x: i * 28 + 6, y: Math.random() * r.height, s: 0.4 + Math.random() * 0.5 });
    }
    function frame(ts) {
      if (!running || window.__MCD_PERF_TIER__ !== 'high') return;
      if (ts - last < gapMs) { requestAnimationFrame(frame); return; }
      last = ts;
      var r = hero.getBoundingClientRect();
      ctx.fillStyle = 'rgba(2,8,5,0.35)';
      ctx.fillRect(0, 0, r.width, r.height);
      ctx.font = '11px monospace';
      ctx.fillStyle = 'rgba(0,230,118,0.18)';
      for (var i = 0; i < cols.length; i++) {
        var c = cols[i];
        ctx.fillText(chars[(Math.random() * chars.length) | 0], c.x, c.y);
        c.y += c.s * 8;
        if (c.y > r.height + 12) { c.y = -12; c.s = 0.4 + Math.random() * 0.5; }
      }
      requestAnimationFrame(frame);
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) running = false;
      else if (window.__MCD_PERF_TIER__ === 'high') {
        running = true;
        last = 0;
        requestAnimationFrame(frame);
      }
    });
    requestAnimationFrame(frame);
  }

  function setupBinaryWind() {
    if (reduce || tier !== 'high' || isMobileLike()) return;
    var host = document.getElementById('mcd-binary-wind');
    if (!host) {
      host = document.createElement('div');
      host.id = 'mcd-binary-wind';
      host.setAttribute('aria-hidden', 'true');
      document.body.appendChild(host);
    }
    function blow() {
      if (document.hidden || window.__MCD_PERF_TIER__ !== 'high') return;
      host.innerHTML = '';
      host.classList.add('is-blowing');
      var frag = document.createDocumentFragment();
      for (var i = 0; i < 8; i++) {
        var bit = document.createElement('span');
        bit.className = 'bit';
        bit.textContent = Math.random() > 0.5 ? '01' : '10';
        bit.style.top = Math.random() * 90 + 'vh';
        bit.style.left = -12 - Math.random() * 10 + 'vw';
        bit.style.fontSize = '11px';
        bit.style.animationDuration = '2.4s';
        frag.appendChild(bit);
      }
      host.appendChild(frag);
      setTimeout(function () {
        host.classList.remove('is-blowing');
        host.innerHTML = '';
      }, 2500);
    }
    setTimeout(blow, 45000);
    setInterval(function () {
      if (!document.hidden && window.__MCD_PERF_TIER__ === 'high') blow();
    }, 180000);
  }

  function boot() {
    document.body.classList.add('mcd-ready');
    applyTier(tier);
    setupHeader();
    if (tier === 'low') return;
    setupReveal();
    setupRipple();
    setupHeroMatrix();
    setupBinaryWind();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
