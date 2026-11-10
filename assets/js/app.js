function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
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
      localStorage.setItem(COMPLETED_KEY, JSON.stringify(items));
    } catch (error) {}
  }

  function bindLessonProgress() {
    const lessonPinButton = document.getElementById('btnPinLesson');
    if (!lessonPinButton) return;
    const lessonUrl = location.pathname + location.search;
    const heading = document.querySelector('main h1');
    const lessonTitle = lessonPinButton.getAttribute('data-title') || (heading ? heading.textContent.trim() : document.title);
    const completeButton = document.createElement('button');
    completeButton.type = 'button';
    completeButton.className = 'btn-complete';
    completeButton.setAttribute('aria-pressed', 'false');
    lessonPinButton.insertAdjacentElement('afterend', completeButton);
    try {
      localStorage.setItem(LAST_LESSON_KEY, JSON.stringify({ url: lessonUrl, title: lessonTitle }));
    } catch (error) {}
    function refreshCompletionState() {
      const isComplete = loadCompletedLessons().some(function (lesson) {
        return lesson.url === lessonUrl;
      });
      completeButton.setAttribute('aria-pressed', String(isComplete));
      completeButton.classList.toggle('is-complete', isComplete);
      completeButton.textContent = isComplete ? '✓ درس تکمیل شد' : 'علامت‌گذاری به‌عنوان تکمیل‌شده';
    }
    completeButton.onclick = function () {
      const completed = loadCompletedLessons();
      const lessonIndex = completed.findIndex(function (lesson) {
        return lesson.url === lessonUrl;
      });
      if (lessonIndex >= 0) completed.splice(lessonIndex, 1);
      else completed.push({ url: lessonUrl, title: lessonTitle });
      saveCompletedLessons(completed);
      refreshCompletionState();
    };
    refreshCompletionState();
  }

  function bindCodeCopyButtons() {
    document.querySelectorAll('.code').forEach(function (codeBlock) {
      const wrapper = codeBlock.closest('.codewrap');
      if (!wrapper || wrapper.querySelector('.code-copy')) return;
      const copyButton = document.createElement('button');
      copyButton.type = 'button';
      copyButton.className = 'code-copy';
      copyButton.textContent = 'کپی کد';
      copyButton.setAttribute('aria-label', 'کپی کد نمونه');
      copyButton.onclick = function () {
        if (!navigator.clipboard) {
          copyButton.textContent = 'کپی در دسترس نیست';
          return;
        }
        navigator.clipboard.writeText(codeBlock.textContent).then(function () {
          copyButton.textContent = 'کپی شد';
          window.setTimeout(function () { copyButton.textContent = 'کپی کد'; }, 1600);
        }).catch(function () {
          copyButton.textContent = 'کپی انجام نشد';
        });
      };
      wrapper.appendChild(copyButton);
    });
  }

  function loadPins() {
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      return Array.isArray(stored)
        ? stored.filter(function (pin) {
            return pin && typeof pin === 'object' && typeof pin.url === 'string';
          })
        : [];
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
    if (badge) badge.textContent = String(loadPins().length);
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
    const pinBtn = document.getElementById('btnPinLesson');
    if (pinBtn) {
      pinBtn.addEventListener('click', function () {
        const url = location.pathname + location.search;
        const heading = document.querySelector('main h1');
        const title = pinBtn.getAttribute('data-title') || (heading ? heading.textContent.trim() : document.title);
        const pins = loadPins();
        const idx = pins.findIndex(function (p) { return p.url === url; });
        if (idx >= 0) pins.splice(idx, 1);
        else pins.unshift({ url: url, title: title });
        savePins(pins);
        updatePinBadge();
      });
    }
    updatePinBadge();
  }

  function boot() {
    bindLessonProgress();
    bindCodeCopyButtons();
    initPins();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
