/*! MCD lesson multiple-choice quiz */
(function () {
  function check(root) {
    var qs = root.querySelectorAll('.q');
    qs.forEach(function (q) {
      var ans = parseInt(q.getAttribute('data-answer'), 10);
      var picked = q.querySelector('input[type=radio]:checked');
      var box = q.querySelector('.result');
      if (!box) return;
      box.hidden = false;
      if (!picked) {
        box.className = 'result bad';
        box.textContent = 'هنوز گزینه‌ای انتخاب نکردی.';
        return;
      }
      var val = parseInt(picked.value, 10);
      if (val === ans) {
        box.className = 'result ok';
        box.textContent = 'درست ✓';
      } else {
        box.className = 'result bad';
        box.textContent = 'غلط — دوباره فکر کن.';
      }
    });
  }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-check]');
    if (!btn) return;
    var id = btn.getAttribute('data-check');
    var root = document.getElementById(id);
    if (root) check(root);
  });
})();
