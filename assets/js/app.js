function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&')
    .replace(/</g, '<')
    .replace(/>/g, '>')
    .replace(/"/g, '"')
    .replace(/'/g, '&#39;');
}

(function () {
  const STORAGE_KEY = 'madrase_pins_v1';
  const COMPLETED_KEY = 'madrase_completed_lessons_v1';
  const LAST_LESSON_KEY = 'madrase_last_lesson_v1';

  function loadCompletedLessons() {
    try {
      const stored = JSON.parse(localStorage.getItem(COMPLETED_KEY) || '[]');
      return Array.isArray(stored)
        ? stored.filter(function (lesson) {
            return lesson && typeof lesson === 'object' && typeof lesson.url === 'string';
          })
        : [];
    } catch (error) {
      return [];
    }
  }

  function saveCompletedLessons(items) {
    try {
      localStorage.setItem(COMPLETED_KEY, JSON.stringify(items.slice(0, 200)));
    } catch (error) {}
  }

  function loadPins() {
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      return Array.isArray(stored) ? stored : [];
    } catch (error) {
      return [];
    }
  }

  function savePins(items) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, 100)));
    } catch (error) {}
  }

  function updatePinBadge() {
    const badge = document.getElementById('pinBadge');
    if (!badge) return;
    const pins = loadPins();
    badge.textContent = String(pins.length);
  }

  function renderPinList() {
    const list = document.getElementById('pinList');
    if (!list) return;
    const pins = loadPins();
    if (!pins.length) {
      list.innerHTML = '<p style="padding:12px;color:#8b949e">هنوز درسی پین نشده است.</p>';
      return;
    }
    list.innerHTML = pins
      .map(function (pin) {
        return (
          '<a href="' +
          escapeHtml(pin.url) +
          '" style="display:block;padding:10px 12px;border-bottom:1px solid #21262d;color:#e6edf3;text-decoration:none">' +
          escapeHtml(pin.title || pin.url) +
          '</a>'
        );
      })
      .join('');
  }

  function initPins() {
    const fab = document.getElementById('pinFab');
    const panel = document.getElementById('pinPanel');
    const closeBtn = document.getElementById('pinPanelClose');
    if (fab && panel) {
      fab.addEventListener('click', function () {
        panel.classList.toggle('open');
        renderPinList();
      });
    }
    if (closeBtn && panel) {
      closeBtn.addEventListener('click', function () {
        panel.classList.remove('open');
      });
    }
    updatePinBadge();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPins);
  } else {
    initPins();
  }

  window.MCD = window.MCD || {};
  window.MCD.loadPins = loadPins;
  window.MCD.savePins = savePins;
  window.MCD.updatePinBadge = updatePinBadge;
})();

/* MCD_APP_OFFLINE_LOADER_V8 — loads download UI only in app mode, all pages */
(function () {
  try {
    var q = location.search || '';
    var path = location.pathname || '';
    var isApp =
      /[?&]mcd=app\b/i.test(q) ||
      /\/app\.html$/i.test(path) ||
      (function () {
        try {
          return sessionStorage.getItem('mcd_app_mode') === '1' || localStorage.getItem('mcd_app_mode') === '1';
        } catch (e) {
          return false;
        }
      })() ||
      (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) ||
      (typeof navigator.standalone === 'boolean' && navigator.standalone === true);
    if (!isApp) return;
    try {
      sessionStorage.setItem('mcd_app_mode', '1');
      localStorage.setItem('mcd_app_mode', '1');
    } catch (e0) {}
    if (window.__MCD_OFFLINE_INIT__) return;
    var s = document.createElement('script');
    s.src = (function () {
      var scripts = document.getElementsByTagName('script');
      for (var i = 0; i < scripts.length; i++) {
        var src = scripts[i].src || '';
        if (/assets\/js\/app\.js/.test(src)) {
          return src.replace(/app\.js.*$/, 'offline-session-v8.js');
        }
      }
      if (path.indexOf('/programer') === 0) return '/programer/assets/js/offline-session-v8.js';
      return 'assets/js/offline-session-v8.js';
    })();
    s.async = true;
    document.head.appendChild(s);
  } catch (e) {}
})();
