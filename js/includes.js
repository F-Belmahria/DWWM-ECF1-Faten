$(document).ready(function () {
  const version = "20260618-footer-text";

  // Load shared layout parts once so every page keeps the same header and footer.
  $("#header").load(`includes/header.html?v=${version}`);
  $("#footer").load(`includes/footer.html?v=${version}`);
});
