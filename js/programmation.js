const showsCards = document.getElementById("showsCards");
const showsCount = document.getElementById("showsCount");

if (showsCards) {
  fetch("assets/data/spectacles.json")
    .then(function (response) {
      if (!response.ok) {
        throw new Error("Fichier JSON introuvable");
      }

      return response.json();
    })
    .then(function (data) {
      showsCards.innerHTML = "";

      data.spectacles.forEach(function (spectacle) {
        createShowCard(spectacle);
      });

      if (showsCount) {
        showsCount.textContent = data.spectacles.length;
      }
    })
    .catch(function (error) {
      console.error("Erreur lors du chargement du fichier JSON :", error);
      showsCards.innerHTML =
        '<p class="programming-list__count">Impossible de charger les spectacles.</p>';
    });
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

  const card = `
    <article class="show-card ${cardClass}">

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
