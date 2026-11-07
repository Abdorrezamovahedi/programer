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
      items.push({ title: title, cat: cat, href: href });
    });
    return items;
  }

  function bindLangSearch(items) {
    var input = document.getElementById("catSearch");
    var grid = document.getElementById("catGrid") || document.querySelector(".cat-grid");
    var results = document.getElementById("catSearchResults");
    if (!input || !results) return;

    if (!items || !items.length) {
      items = collectFromDom();
    }

    function run() {
      var q = (input.value || "").trim().toLowerCase();
      if (!q) {
        results.classList.add("is-hidden");
        results.innerHTML = "";
        if (grid) grid.classList.remove("is-hidden");
        return;
      }
      if (grid) grid.classList.add("is-hidden");
      results.classList.remove("is-hidden");
      var html = "";
      var found = 0;
      items.forEach(function (it) {
        var hay = ((it.title || "") + " " + (it.cat || "") + " " + (it.href || "")).toLowerCase();
        if (hay.indexOf(q) === -1) return;
        found++;
        html +=
          '<a class="lesson-list-item lang-link" href="' +
          esc(it.href) +
          '"><span>' +
          esc(it.title) +
          '</span><small style="color:#8b949e">' +
          esc(it.cat) +
          "</small></a>";
      });
      results.innerHTML = found
        ? html
        : '<div class="ex-empty">نتیجه‌ای پیدا نشد.</div>';
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
