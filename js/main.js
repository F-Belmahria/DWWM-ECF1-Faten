const featuredCarousel = document.querySelector(".featured-shows");
const showsGrid = document.getElementById("showsGrid");
const showsPrev = document.getElementById("showsPrev");
const showsNext = document.getElementById("showsNext");
const mobileCarouselQuery = window.matchMedia("(max-width: 767.98px)");

let activeShowIndex = 0;

if (featuredCarousel && showsGrid && showsPrev && showsNext) {
  // Store the cards once so the carousel can reuse the same elements.
  const showCards = Array.from(showsGrid.querySelectorAll(".show-card"));
  const paginationButtons = Array.from(
    featuredCarousel.querySelectorAll(".shows-pagination__button")
  );

  function updateFeaturedCarousel() {
    const isMobile = mobileCarouselQuery.matches;

    // On mobile, only one card is visible. On larger screens, all cards remain visible.
    showCards.forEach(function (card, index) {
      if (!isMobile) {
        card.style.display = "";
        return;
      }

      card.style.display = index === activeShowIndex ? "block" : "none";
    });

    paginationButtons.forEach(function (button, index) {
      const isActive = index === activeShowIndex;

      // Keep the visual active dot and the accessibility state synchronized.
      button.classList.toggle("shows-pagination__button--active", isActive);
      button.setAttribute("aria-current", isActive ? "true" : "false");
    });
  }

  function goToShow(index) {
    // Modulo keeps navigation looping from the last card back to the first one.
    activeShowIndex = (index + showCards.length) % showCards.length;
    updateFeaturedCarousel();
  }

  function scrollDesktopCarousel(direction) {
    const firstCard = showCards[0];
    const gridStyles = window.getComputedStyle(showsGrid);
    const gap = parseFloat(gridStyles.columnGap) || 0;
    // The scroll distance matches exactly one card plus the CSS grid gap.
    const scrollAmount = firstCard.offsetWidth + gap;

    showsGrid.scrollBy({
      left: direction * scrollAmount,
      behavior: "smooth",
    });
  }

  showsPrev.addEventListener("click", function () {
    // Mobile uses card switching, desktop uses horizontal scrolling.
    if (mobileCarouselQuery.matches) {
      goToShow(activeShowIndex - 1);
      return;
    }

    scrollDesktopCarousel(-1);
  });

  showsNext.addEventListener("click", function () {
    // Mobile uses card switching, desktop uses horizontal scrolling.
    if (mobileCarouselQuery.matches) {
      goToShow(activeShowIndex + 1);
      return;
    }

    scrollDesktopCarousel(1);
  });

  paginationButtons.forEach(function (button, index) {
    button.addEventListener("click", function () {
      // On desktop, pagination scrolls to the matching card instead of hiding cards.
      if (!mobileCarouselQuery.matches) {
        const targetCard = showCards[index];

        if (targetCard) {
          showsGrid.scrollTo({
            left: targetCard.offsetLeft - showsGrid.offsetLeft,
            behavior: "smooth",
          });
        }

        return;
      }

      goToShow(index);
    });
  });

  mobileCarouselQuery.addEventListener("change", updateFeaturedCarousel);
  // Initialize the carousel once the listeners are ready.
  updateFeaturedCarousel();
}
