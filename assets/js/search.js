function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

(function () {
  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function norm(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/ي/g, "ی")
      .replace(/ك/g, "ک")
      .replace(/‌/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function collectFromDom() {
    var items = [];
    var root = document.getElementById("catGrid") || document.querySelector(".cat-grid") || document.querySelector(".langs");
    if (!root) return items;
    root.querySelectorAll("a").forEach(function (a) {
      var href = a.getAttribute("href") || "";
      if (!href || href === "#" || href.indexOf("javascript:") === 0) return;
      var title = (a.querySelector("b") && a.querySelector("b").textContent) || a.textContent || "";
      title = title.replace(/\s+/g, " ").trim();
      var cat = (a.querySelector("small") && a.querySelector("small").textContent) || "";
      cat = cat.replace(/\s+/g, " ").trim();
      if (!title) return;
      items.push({ title: title, cat: cat, href: href, keys: title + " " + cat });
    });
    return items;
  }

  function bindLangSearch(items) {
    var input = document.getElementById("catSearch");
    var grid = document.getElementById("catGrid") || document.querySelector(".cat-grid");
    var results = document.getElementById("catSearchResults");
    if (!input || !results) return;

    if (!items || !items.length) {
      if (window.LANG_SEARCH_ITEMS && window.LANG_SEARCH_ITEMS.length) {
        items = window.LANG_SEARCH_ITEMS;
      } else {
        items = collectFromDom();
      }
    }

    function run() {
      var q = norm(input.value || "");
      if (!q) {
        results.classList.add("is-hidden");
        results.innerHTML = "";
        if (grid) grid.classList.remove("is-hidden");
        return;
      }
      if (grid) grid.classList.add("is-hidden");
      results.classList.remove("is-hidden");

      var parts = q.split(" ").filter(Boolean);
      var html = "";
      var found = 0;
      items.forEach(function (it) {
        var hay = norm((it.title || "") + " " + (it.cat || "") + " " + (it.keys || "") + " " + (it.href || ""));
        var ok = true;
        for (var i = 0; i < parts.length; i++) {
          if (hay.indexOf(parts[i]) === -1) {
            ok = false;
            break;
          }
        }
        if (!ok) return;
        found++;
        html +=
          '<a class="lesson-list-item lang-link" href="' +
          esc(it.href) +
          '"><span>' +
          esc(it.title) +
          '</span><small style="color:#8b949e">' +
          esc(it.cat || "") +
          "</small></a>";
      });
      results.innerHTML = found
        ? html
        : '<div class="ex-empty">نتیجه‌ای پیدا نشد. کلمه دیگری مثل «متغیر» یا «regex» را امتحان کن.</div>';
    }

    input.addEventListener("input", run);
    input.addEventListener("search", run);
  }

  window.bindLangSearch = bindLangSearch;

  document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("catSearch")) {
      bindLangSearch();
    }
  });
})();
