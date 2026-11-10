/**
 * DISABLED on normal site (Google).
 * Offline UI is only loaded from offline-session-v8.js when opened via app.html / ?mcd=app.
 */
(function () {
  try {
    ["mcd-offline-nav", "mcd-offline-modal", "mcd-offline-fab", "mcd-page-save"].forEach(function (id) {
      var el = document.getElementById(id);
      if (el && el.parentNode) el.parentNode.removeChild(el);
    });
  } catch (e) {}
})();
