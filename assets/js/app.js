(function () {
  const STORAGE_KEY = 'madrase_pins_v1';
  const COMPLETED_KEY = 'madrase_completed_lessons_v1';
  const LAST_LESSON_KEY = 'madrase_last_lesson_v1';

  function loadCompletedLessons() {
    try {
      return JSON.parse(localStorage.getItem(COMPLETED_KEY) || '[]');
    } catch (error) {
      return [];
    }
  }

  function saveCompletedLessons(items) {
    try {
      localStorage.setItem(COMPLETED_KEY, JSON.stringify(items));
    } catch (error) {
      // Ignore storage issues gracefully.
    }
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
    } catch (error) {
      // Progress remains available when storage is enabled.
    }

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

      if (lessonIndex >= 0) {
        completed.splice(lessonIndex, 1);
      } else {
        completed.push({ url: lessonUrl, title: lessonTitle });
      }

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
        const codeText = codeBlock.textContent;
        if (!navigator.clipboard) {
          copyButton.textContent = 'کپی در دسترس نیست';
          return;
        }

        navigator.clipboard.writeText(codeText).then(function () {
          copyButton.textContent = 'کپی شد';
          window.setTimeout(function () {
            copyButton.textContent = 'کپی کد';
          }, 1600);
        }).catch(function () {
          copyButton.textContent = 'کپی انجام نشد';
        });
      };
      wrapper.appendChild(copyButton);
    });
  }

  function bindLessonActions() {
    const lessonPinButton = document.getElementById('btnPinLesson');
    if (!lessonPinButton) return;

    const actions = document.createElement('div');
    actions.className = 'lesson-utility-actions';

    const printButton = document.createElement('button');
    printButton.type = 'button';
    printButton.textContent = 'چاپ درس';
    printButton.onclick = function () {
      window.print();
    };

    const shareButton = document.createElement('button');
    shareButton.type = 'button';
    shareButton.textContent = 'اشتراک‌گذاری';
    shareButton.onclick = function () {
      const shareData = { title: document.title, url: location.href };
      if (navigator.share) {
        navigator.share(shareData).catch(function () {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(location.href).then(function () {
          shareButton.textContent = 'پیوند کپی شد';
        });
      }
    };

    actions.append(printButton, shareButton);
    lessonPinButton.insertAdjacentElement('afterend', actions);
  }

  function loadPins() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch (error) {
      return [];
    }
  }

  function savePins(items) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
    } catch (error) {
      // Ignore storage issues gracefully.
    }
  }

  function isPinned(url) {
    return loadPins().some(function (pin) {
      return pin.k === url;
    });
  }

  function togglePin(url, title, category) {
    const pins = loadPins();
    const pinIndex = pins.findIndex(function (pin) {
      return pin.k === url;
    });

    if (pinIndex >= 0) {
      pins.splice(pinIndex, 1);
    } else {
      pins.unshift({
        k: url,
        url: url,
        title: title,
        cat: category || '',
        at: Date.now(),
      });

      if (pins.length > 50) {
        pins.length = 50;
      }
    }

    savePins(pins);
    updatePinBadge();

    return pinIndex < 0;
  }

  function updatePinBadge() {
    const badge = document.getElementById('pinBadge');
    if (badge) {
      badge.textContent = String(loadPins().length);
    }
  }

  function renderPinnedList() {
    const panelList = document.getElementById('pinList');
    if (!panelList) return;

    const pins = loadPins();
    if (!pins.length) {
      panelList.innerHTML = '<div class=pin-empty>خالی</div>';
      return;
    }

    panelList.innerHTML = '';
    pins.forEach(function (pin) {
      const item = document.createElement('div');
      item.className = 'pin-item';
      item.innerHTML = '<div class=meta><b></b><small></small></div><button type=button class=unpin>برداشتن</button>';

      item.querySelector('b').textContent = pin.title;
      item.querySelector('small').textContent = pin.cat || '';

      item.querySelector('.meta').onclick = function () {
        location.href = pin.url;
      };

      item.querySelector('.unpin').onclick = function (event) {
        event.stopPropagation();
        togglePin(pin.k, pin.title, pin.cat);
        renderPinnedList();
      };

      panelList.appendChild(item);
    });
  }

  function bindLessonPinButton() {
    const lessonPinButton = document.getElementById('btnPinLesson');
    if (!lessonPinButton) return;

    const lessonUrl = location.pathname + location.search;
    const lessonTitle = lessonPinButton.getAttribute('data-title') || document.title;
    const lessonCategory = lessonPinButton.getAttribute('data-cat') || '';

    function refreshLessonPinState() {
      const isSelected = isPinned(lessonUrl);
      lessonPinButton.classList.toggle('on', isSelected);
      lessonPinButton.textContent = isSelected ? '📌 پین‌شده' : '📌 پین کردن این درس';
    }

    lessonPinButton.onclick = function () {
      togglePin(lessonUrl, lessonTitle, lessonCategory);
      refreshLessonPinState();
    };

    refreshLessonPinState();
  }

  function bindEditorButtons() {
    document.querySelectorAll('.trybtn').forEach(function (button) {
      button.onclick = function () {
        const codeBlock = button.previousElementSibling;
        const codeElement = codeBlock && codeBlock.querySelector ? codeBlock.querySelector('.code') : codeBlock;
        const editorOverlay = document.getElementById('edBack');
        const editorCode = document.getElementById('edCode');

        if (editorOverlay && editorCode) {
          editorCode.textContent = codeElement ? codeElement.textContent : '';
          editorOverlay.style.display = 'flex';
        }
      };
    });
  }

  function bindEditorCloseActions() {
    const closeButton = document.getElementById('edClose');
    const editorOverlay = document.getElementById('edBack');
    const copyButton = document.getElementById('edCopy');

    if (closeButton) {
      closeButton.onclick = function () {
        if (editorOverlay) editorOverlay.style.display = 'none';
      };
    }

    if (editorOverlay) {
      editorOverlay.onclick = function (event) {
        if (event.target.id === 'edBack') {
          editorOverlay.style.display = 'none';
        }
      };
    }

    if (copyButton && editorOverlay) {
      copyButton.onclick = function () {
        const codeText = document.getElementById('edCode')?.textContent || '';
        if (navigator.clipboard) {
          navigator.clipboard.writeText(codeText);
        }
      };
    }
  }

  function bindQuizCards() {
    document.querySelectorAll('.qcard[data-quiz]').forEach(function (card) {
      if (card.getAttribute('data-bound')) return;
      card.setAttribute('data-bound', '1');

      const feedbackBox = card.querySelector('.qfb');
      card.querySelectorAll('.qopt').forEach(function (optionButton) {
        optionButton.onclick = function () {
          if (card.getAttribute('data-done')) return;
          card.setAttribute('data-done', '1');

          const isCorrect = optionButton.getAttribute('data-correct') === '1';
          card.querySelectorAll('.qopt').forEach(function (button) {
            button.disabled = true;
            if (button.getAttribute('data-correct') === '1') {
              button.classList.add('ok');
            }
          });

          if (!isCorrect) optionButton.classList.add('bad');

          if (feedbackBox) {
            feedbackBox.textContent = optionButton.getAttribute('data-exp') || '';
            feedbackBox.classList.add('on');
            feedbackBox.classList.add(isCorrect ? 'ok-msg' : 'bad-msg');
          }
        };
      });
    });
  }

  function startApp() {
    const pinFab = document.getElementById('pinFab');
    const pinPanel = document.getElementById('pinPanel');

    if (pinFab && pinPanel) {
      pinFab.onclick = function () {
        pinPanel.classList.toggle('on');
        if (pinPanel.classList.contains('on')) {
          renderPinnedList();
        }
      };

      const closeButton = document.getElementById('pinPanelClose');
      if (closeButton) {
        closeButton.onclick = function () {
          pinPanel.classList.remove('on');
        };
      }

      updatePinBadge();
    }

    bindLessonPinButton();
    bindLessonProgress();
    bindCodeCopyButtons();
    bindLessonActions();
    bindEditorButtons();
    bindEditorCloseActions();
    bindQuizCards();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startApp);
  } else {
    startApp();
  }
})();
