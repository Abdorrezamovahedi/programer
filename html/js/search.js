(function () {
  const input = document.getElementById("lessonSearch");
  const links = document.querySelectorAll("#sideMenu a[data-title]");
  if (!input || !links.length) return;

  input.addEventListener("input", function () {
    const q = this.value.trim().toLowerCase();
    links.forEach(function (a) {
      const title = (a.getAttribute("data-title") || a.textContent || "").toLowerCase();
      if (!q || title.indexOf(q) !== -1) {
        a.classList.remove("hidden");
      } else {
        a.classList.add("hidden");
      }
    });
  });
})();
