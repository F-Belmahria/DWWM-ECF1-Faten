const showsCards = document.getElementById("showsCards");
const showsCount = document.getElementById("showsCount");
const showsFilters = document.getElementById("showsFilters");
const typeFilter = document.getElementById("typeFilter");
const dateFilter = document.getElementById("dateFilter");
const availabilityFilter = document.getElementById("availabilityFilter");
const resetFilters = document.getElementById("resetFilters");
const sortShows = document.getElementById("sortShows");
const dataVersion = "20260619-show-eight-3";

let allSpectacles = [];

if (showsCards) {
  fetch(`assets/data/spectacles.json?v=${dataVersion}`)
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Fichier JSON introuvable");
      }

      return response.json();
    })
    .then(function (data) {
      // Keep the page display limited to eight cards, even if an old JSON cache has more.
      allSpectacles = data.spectacles.slice(0, 8);

      setupDatePicker(allSpectacles);
      setupFilters();
      applyFilters();
    })
    .catch(function (error) {
      console.error("Erreur lors du chargement du fichier JSON :", error);
      showsCards.innerHTML =
        '<p class="programming-list__count">Impossible de charger les spectacles.</p>';
    });
}

function setupFilters() {
  if (showsFilters) {
    showsFilters.addEventListener("submit", function (event) {
      event.preventDefault();
      applyFilters();
    });
  }

  [typeFilter, dateFilter, availabilityFilter, sortShows].forEach(function (
    filter
  ) {
    if (filter) {
      filter.addEventListener("change", applyFilters);
    }
  });

  if (resetFilters) {
    resetFilters.addEventListener("click", function () {
      if (typeFilter) {
        typeFilter.value = "all";
      }

      if (dateFilter) {
        dateFilter.value = "";
      }

      if (availabilityFilter) {
        availabilityFilter.value = "all";
      }

      if (sortShows) {
        sortShows.value = "date-asc";
      }

      applyFilters();
    });
  }
}

function applyFilters() {
  let filteredSpectacles = allSpectacles.filter(function (spectacle) {
    const matchType =
      !typeFilter ||
      typeFilter.value === "all" ||
      spectacle.type === typeFilter.value;

    const matchDate =
      !dateFilter ||
      dateFilter.value === "" ||
      spectacle.date === dateFilter.value;

    const matchAvailability =
      !availabilityFilter ||
      availabilityFilter.value === "all" ||
      getAvailability(spectacle) === availabilityFilter.value;

    return matchType && matchDate && matchAvailability;
  });

  // Apply sorting after filtering so the visible cards stay in the right order.
  filteredSpectacles = sortSpectacles(filteredSpectacles);

  renderShows(filteredSpectacles);
}

function renderShows(spectacles) {
  showsCards.innerHTML = "";

  if (spectacles.length === 0) {
    showsCards.innerHTML =
      '<p class="programming-list__count">Aucun spectacle trouve.</p>';
  } else {
    spectacles.forEach(function (spectacle) {
      createShowCard(spectacle);
    });
  }

  if (showsCount) {
    showsCount.textContent = spectacles.length;
  }
}

function setupDatePicker(spectacles) {
  if (!dateFilter) {
    return;
  }

  const dates = [];

  spectacles.forEach(function (spectacle) {
    if (!dates.includes(spectacle.date)) {
      dates.push(spectacle.date);
    }
  });

  dates.sort();

  // Limit the calendar to the show period from the JSON file.
  dateFilter.min = dates[0];
  dateFilter.max = dates[dates.length - 1];
}

function sortSpectacles(spectacles) {
  const sortValue = sortShows ? sortShows.value : "date-asc";
  const sortedSpectacles = spectacles.slice();

  sortedSpectacles.sort(function (first, second) {
    if (sortValue === "date-desc") {
      return second.date.localeCompare(first.date);
    }

    if (sortValue === "price-asc") {
      return first.prix - second.prix;
    }

    if (sortValue === "price-desc") {
      return second.prix - first.prix;
    }

    return first.date.localeCompare(second.date);
  });

  return sortedSpectacles;
}

function getAvailability(spectacle) {
  const placesRestantes = spectacle.places_total - spectacle.places_vendues;

  if (placesRestantes === 0) {
    return "soldout";
  }

  if (placesRestantes <= 20) {
    return "few";
  }

  return "available";
}

function createShowCard(spectacle) {
  const placesTotal = spectacle.places_total;
  const placesVendues = spectacle.places_vendues;
  const placesRestantes = placesTotal - placesVendues;

  const pourcentage = (placesVendues / placesTotal) * 100;

  let statut = "";
  let statutClass = "";
  let cardClass = "";

  if (placesRestantes === 0) {
    statut = "Complet";
    statutClass = "sold-out";
    cardClass = "card-sold-out";
  } else if (placesRestantes <= 20) {
    statut = "Quelques places";
    statutClass = "few-left";
    cardClass = "card-available";
  } else {
    statut = "Disponible";
    statutClass = "available";
    cardClass = "card-available";
  }

  const dateInfo = formatDate(spectacle.date);
  const typeText = formatType(spectacle.type);

  let imagePart = "";

  if (spectacle.image !== "") {
    imagePart = `
  <img 
    class="show-card-image" 
    src="${getImagePath(spectacle.image)}" 
    alt="${spectacle.titre}"
  >
`;
  } else {
    imagePart = `
      <div class="image-placeholder">
        <span>${typeText}</span>
      </div>
    `;
  }
  const isSoldOut = placesRestantes === 0;
  const card = `
    <article 
  class="show-card ${cardClass}"
  data-type="${spectacle.type}"
  data-date="${spectacle.date}"
  data-soldout="${isSoldOut}"
>

      <div class="show-card-header">
        ${imagePart}

        <div class="date-badge">
          <span>${dateInfo.jour}</span>
          <small>${dateInfo.mois}</small>
        </div>

        <div class="favorite-icon">
          ♡
        </div>
      </div>

      <div class="show-card-body">
        <span class="type-badge">${typeText}</span>

        <h2>${spectacle.titre}</h2>

        <p class="artist">
          ${spectacle.artiste}
        </p>

        <div class="show-infos">
          <span>🕘 ${spectacle.horaire}</span>
          <span>⏱ ${spectacle.duree}</span>
        </div>

        <div class="price">
          ${spectacle.prix} €
        </div>

        <p class="status ${statutClass}">
          ● ${statut}
        </p>

        <div class="progress">
          <div 
            class="progress-bar ${statutClass}" 
            style="width: ${pourcentage}%">
          </div>
        </div>

        <p class="places">
          ${placesVendues} / ${placesTotal} places vendues
        </p>

      </div>

    </article>
  `;

  showsCards.innerHTML += card;
}

function formatDate(dateText) {
  const parts = dateText.split("-");
  const moisNumero = Number(parts[1]);
  const jour = parts[2];

  const moisListe = [
    "JAN",
    "FÉV",
    "MAR",
    "AVR",
    "MAI",
    "JUIN",
    "JUIL",
    "AOÛT",
    "SEP",
    "OCT",
    "NOV",
    "DÉC",
  ];

  return {
    jour: jour,
    mois: moisListe[moisNumero - 1],
  };
}

function formatType(type) {
  if (type === "theatre") {
    return "THÉÂTRE";
  }

  if (type === "concert") {
    return "MUSIQUE";
  }

  if (type === "standup") {
    return "HUMOUR";
  }

  return type.toUpperCase();
}

function getImagePath(image) {
  if (image.startsWith("assets/")) {
    return image;
  }

  if (image.startsWith("images/")) {
    return image.replace("images/", "assets/images/");
  }

  return `assets/images/${image}`;
}
