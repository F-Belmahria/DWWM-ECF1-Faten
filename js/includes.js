$(document).ready(function () {
  const version = "20260618-footer-text";

  $("#header").load(`includes/header.html?v=${version}`);
  $("#footer").load(`includes/footer.html?v=${version}`);
});
