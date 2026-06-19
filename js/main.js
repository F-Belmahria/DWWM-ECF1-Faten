const featuredCarousel = document.querySelector(".featured-shows");
const showsGrid = document.getElementById("showsGrid");
const showsPrev = document.getElementById("showsPrev");
const showsNext = document.getElementById("showsNext");
const mobileCarouselQuery = window.matchMedia("(max-width: 767.98px)");

let activeShowIndex = 0;

if (featuredCarousel && showsGrid && showsPrev && showsNext) {
  const showCards = Array.from(showsGrid.querySelectorAll(".show-card"));
  const paginationButtons = Array.from(
    featuredCarousel.querySelectorAll(".shows-pagination__button")
  );

  function updateFeaturedCarousel() {
    const isMobile = mobileCarouselQuery.matches;

    showCards.forEach(function (card, index) {
      if (!isMobile) {
        card.style.display = "";
        return;
      }

      card.style.display = index === activeShowIndex ? "block" : "none";
    });

    paginationButtons.forEach(function (button, index) {
      const isActive = index === activeShowIndex;

      button.classList.toggle("shows-pagination__button--active", isActive);
      button.setAttribute("aria-current", isActive ? "true" : "false");
    });
  }

  function goToShow(index) {
    activeShowIndex = (index + showCards.length) % showCards.length;
    updateFeaturedCarousel();
  }

  function scrollDesktopCarousel(direction) {
    const firstCard = showCards[0];
    const gridStyles = window.getComputedStyle(showsGrid);
    const gap = parseFloat(gridStyles.columnGap) || 0;
    const scrollAmount = firstCard.offsetWidth + gap;

    showsGrid.scrollBy({
      left: direction * scrollAmount,
      behavior: "smooth",
    });
  }

  showsPrev.addEventListener("click", function () {
    if (mobileCarouselQuery.matches) {
      goToShow(activeShowIndex - 1);
      return;
    }

    scrollDesktopCarousel(-1);
  });

  showsNext.addEventListener("click", function () {
    if (mobileCarouselQuery.matches) {
      goToShow(activeShowIndex + 1);
      return;
    }

    scrollDesktopCarousel(1);
  });

  paginationButtons.forEach(function (button, index) {
    button.addEventListener("click", function () {
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
  updateFeaturedCarousel();
}
