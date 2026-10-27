(function () {
  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function bindLangSearch(items) {
    var input = document.getElementById("catSearch");
    var grid = document.getElementById("catGrid");
    var results = document.getElementById("catSearchResults");
    if (!input || !grid || !results) return;

    input.addEventListener("input", function () {
      var q = (this.value || "").trim().toLowerCase();
      if (!q) {
        results.classList.add("is-hidden");
        results.innerHTML = "";
        grid.classList.remove("is-hidden");
        return;
      }

      grid.classList.add("is-hidden");
      results.classList.remove("is-hidden");
      var html = "",
        found = 0;
      items.forEach(function (it) {
        if ((it.title + " " + it.cat).toLowerCase().indexOf(q) === -1) return;
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
    });
  }
  window.bindLangSearch = bindLangSearch;
})();
