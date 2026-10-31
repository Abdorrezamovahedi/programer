/**
 * فیلتر تمرین‌ها: جست‌وجوی نام + سطح سختی + مبحث
 * انتظار: هر li دارای data-title, data-level, data-topic
 * و داخل صفحه: #exSearch, #exLevel, #exTopic, #exList, #exEmpty, #exCount
 */
(function () {
  function norm(s) {
    return (s || "")
      .toString()
      .trim()
      .toLowerCase()
      .replace(/ي/g, "ی")
      .replace(/ك/g, "ک");
  }

  function init() {
    var list = document.getElementById("exList");
    if (!list) return;
    var items = Array.prototype.slice.call(list.querySelectorAll("li[data-title]"));
    if (!items.length) return;

    var search = document.getElementById("exSearch");
    var level = document.getElementById("exLevel");
    var topic = document.getElementById("exTopic");
    var empty = document.getElementById("exEmpty");
    var count = document.getElementById("exCount");

    // پر کردن گزینه‌های مبحث از خود لیست
    if (topic) {
      var topics = {};
      items.forEach(function (li) {
        var t = (li.getAttribute("data-topic") || "").trim();
        if (t) topics[t] = true;
      });
      var keys = Object.keys(topics).sort(function (a, b) {
        return a.localeCompare(b, "fa");
      });
      keys.forEach(function (t) {
        var opt = document.createElement("option");
        opt.value = t;
        opt.textContent = t;
        topic.appendChild(opt);
      });
    }

    function apply() {
      var q = norm(search && search.value);
      var lv = level ? level.value : "";
      var tp = topic ? topic.value : "";
      var shown = 0;

      items.forEach(function (li) {
        var title = norm(li.getAttribute("data-title"));
        var itemLevel = li.getAttribute("data-level") || "";
        var itemTopic = li.getAttribute("data-topic") || "";
        var ok = true;
        if (q && title.indexOf(q) === -1) ok = false;
        if (lv && itemLevel !== lv) ok = false;
        if (tp && itemTopic !== tp) ok = false;
        li.style.display = ok ? "" : "none";
        if (ok) shown++;
      });

      if (empty) empty.hidden = shown !== 0;
      if (count) count.textContent = shown;
    }

    if (search) search.addEventListener("input", apply);
    if (level) level.addEventListener("change", apply);
    if (topic) topic.addEventListener("change", apply);
    apply();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
