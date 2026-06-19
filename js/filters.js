const filterTypeButtons = document.querySelectorAll("[data-filter-type]");
const filterDateButtons = document.querySelectorAll("[data-filter-date]");
const hideSoldOutInput = document.getElementById("hideSoldOut");
const showsCountElement = document.getElementById("showsCount");

let selectedType = "all";
let selectedDate = "all";

filterTypeButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    selectedType = button.dataset.filterType;

    filterTypeButtons.forEach(function (btn) {
      btn.classList.remove("is-active");
    });

    button.classList.add("is-active");

    applyFilters();
  });
});

filterDateButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    selectedDate = button.dataset.filterDate;

    filterDateButtons.forEach(function (btn) {
      btn.classList.remove("is-active");
    });

    button.classList.add("is-active");

    applyFilters();
  });
});

if (hideSoldOutInput) {
  hideSoldOutInput.addEventListener("change", function () {
    applyFilters();
  });
}

function applyFilters() {
  const cards = document.querySelectorAll(".show-card");
  let visibleCount = 0;

  cards.forEach(function (card) {
    const cardType = card.dataset.type;
    const cardDate = card.dataset.date;
    const cardSoldOut = card.dataset.soldout === "true";

    const matchType = selectedType === "all" || cardType === selectedType;
    const matchDate = selectedDate === "all" || cardDate === selectedDate;
    const matchAvailability = !hideSoldOutInput.checked || !cardSoldOut;

    if (matchType && matchDate && matchAvailability) {
      card.style.display = "block";
      visibleCount++;
    } else {
      card.style.display = "none";
    }
  });

  if (showsCountElement) {
    showsCountElement.textContent = visibleCount;
  }
}
