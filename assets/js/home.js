(function () {
  const COMPLETED_KEY = 'madrase_completed_lessons_v1';
  const LAST_LESSON_KEY = 'madrase_last_lesson_v1';
  let searchIndexPromise;

  function safeRead(key, fallback) {
    try {
      const value = JSON.parse(localStorage.getItem(key) || 'null');
      return value === null ? fallback : value;
    } catch (error) {
      return fallback;
    }
  }

  function renderProgress() {
    const summary = document.getElementById('homeProgressSummary');
    const continueLink = document.getElementById('continueLearning');
    if (!summary || !continueLink) return;

    const completed = safeRead(COMPLETED_KEY, []);
    const lastLesson = safeRead(LAST_LESSON_KEY, null);
    summary.textContent = completed.length
      ? `${completed.length} درس را تکمیل کرده‌ای. هر زمان خواستی می‌توانی مرورشان کنی.`
      : 'هنوز درسی را تکمیل نکرده‌ای. یک درس را شروع کن و پس از مطالعه، آن را تکمیل‌شده علامت بزن.';

    if (lastLesson && lastLesson.url && lastLesson.title) {
      continueLink.href = lastLesson.url;
      continueLink.textContent = `ادامه: ${lastLesson.title} ←`;
    }
  }

  function normalize(value) {
    return value
      .normalize('NFKC')
      .toLocaleLowerCase('fa')
      .replace(/[يى]/g, 'ی')
      .replace(/ك/g, 'ک')
      .replace(/[\u064B-\u065F\u0670]/g, '')
      .replace(/[-_]+/g, ' ')
      .trim();
  }

  function languageName(path) {
    const section = path.split('/')[0];
    const names = {
      python: 'Python',
      html: 'HTML',
      css: 'CSS',
      javascript: 'JavaScript',
      php: 'PHP',
      tamrin: 'تمرین',
    };
    return names[section] || 'آموزش';
  }

  function titleFromPath(path) {
    const segments = decodeURIComponent(path).split('/');
    let title = segments[segments.length - 1];
    if (title === 'index.html') title = segments[segments.length - 2] || 'صفحهٔ اصلی';
    title = title.replace(/\.html?$/i, '').replace(/^\d+[-_.\s]*/, '').replace(/[-_]+/g, ' ');
    return title || 'صفحهٔ آموزشی';
  }

  function loadSearchIndex() {
    if (!searchIndexPromise) {
      const sitemapUrl = new URL('sitemap.xml', document.baseURI);
      searchIndexPromise = fetch(sitemapUrl)
        .then(function (response) {
          if (!response.ok) throw new Error('sitemap unavailable');
          return response.text();
        })
        .then(function (xml) {
          const documentXml = new DOMParser().parseFromString(xml, 'application/xml');
          const canonical = document.querySelector('link[rel="canonical"]');
          const sitePath = canonical ? new URL(canonical.href).pathname : new URL('./', document.baseURI).pathname;
          return Array.from(documentXml.querySelectorAll('loc'))
            .map(function (locationElement) {
              const url = new URL(locationElement.textContent.trim(), document.baseURI);
              if (!url.pathname.startsWith(sitePath)) return null;
              const path = url.pathname.slice(sitePath.length);
              const title = titleFromPath(path);
              return { path: path, title: title, language: languageName(path), text: normalize(`${title} ${path}`) };
            })
            .filter(Boolean);
        });
    }
    return searchIndexPromise;
  }

  function renderResults(results, list) {
    list.replaceChildren();
    results.slice(0, 12).forEach(function (result) {
      const item = document.createElement('li');
      const link = document.createElement('a');
      const title = document.createElement('b');
      const category = document.createElement('small');

      link.href = result.path;
      title.textContent = result.title;
      category.textContent = result.language;
      link.append(title, category);
      item.appendChild(link);
      list.appendChild(item);
    });
  }

  function bindSearch() {
    const form = document.getElementById('homeSearchForm');
    const input = document.getElementById('homeSearch');
    const status = document.getElementById('homeSearchStatus');
    const resultsList = document.getElementById('homeSearchResults');
    if (!form || !input || !status || !resultsList) return;

    let searchTimer;
    function search() {
      const query = normalize(input.value);
      if (!query) {
        resultsList.classList.add('is-hidden');
        resultsList.replaceChildren();
        status.textContent = 'عنوان درس‌ها و مسیرهای آموزشی را جستجو کن.';
        return;
      }

      status.textContent = 'در حال جستجو در عنوان درس‌ها...';
      loadSearchIndex()
        .then(function (index) {
          const matches = index.filter(function (item) {
            return item.text.includes(query);
          });
          renderResults(matches, resultsList);
          resultsList.classList.toggle('is-hidden', matches.length === 0);
          status.textContent = matches.length
            ? `${Math.min(matches.length, 12)} نتیجه از ${matches.length} عنوان پیدا شد.`
            : 'نتیجه‌ای در عنوان درس‌ها پیدا نشد. نام زبان یا موضوع را کوتاه‌تر بنویس.';
        })
        .catch(function () {
          resultsList.classList.add('is-hidden');
          status.textContent = 'فهرست جستجو بارگذاری نشد؛ اتصال به سایت را بررسی و دوباره تلاش کن.';
        });
    }

    input.addEventListener('input', function () {
      window.clearTimeout(searchTimer);
      searchTimer = window.setTimeout(search, 140);
    });
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      window.clearTimeout(searchTimer);
      search();
    });
  }

  renderProgress();
  bindSearch();
})();
