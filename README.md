# Le Phosphore - Performing Arts Venue Website

## Project Overview

Le Phosphore is a responsive website created for a fictional performing arts venue.  
The venue hosts theatre plays, concerts, stand-up shows, and live performances.

This project was created as part of the DWWM front-end assessment. It focuses on:

- HTML structure
- Sass/CSS styling
- BEM naming methodology
- Responsive design
- JavaScript interactions
- JSON-based show data
- Accessibility and eco-design awareness

## Pages

The website contains three main pages:

- `index.html` - Homepage with hero section, featured shows, venue presentation, practical info blocks, and newsletter section.
- `programmation.html` - Show listing page with dynamic cards generated from JSON.
- `infos-pratiques.html` - Practical information page.

Reusable header and footer files are stored in:

- `includes/header.html`
- `includes/footer.html`

They are loaded with JavaScript from `js/includes.js`.

## Technologies Used

- HTML5
- Sass / SCSS
- CSS3
- JavaScript
- JSON
- Bootstrap 5
- Bootstrap Icons
- Google Fonts
- Git and GitHub
- Live Server

## Project Structure

```text
DWWM-ECF1-Faten/
|-- assets/
|   |-- data/
|   |   `-- spectacles.json
|   `-- images/
|-- css/
|   `-- style.css
|-- includes/
|   |-- header.html
|   `-- footer.html
|-- js/
|   |-- includes.js
|   |-- main.js
|   `-- programmation.js
|-- scss/
|   |-- base/
|   |-- components/
|   |-- pages/
|   `-- style.scss
|-- index.html
|-- programmation.html
|-- infos-pratiques.html
|-- package.json
`-- README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Open the project folder:

```bash
cd DWWM-ECF1-Faten
```

Install dependencies:

```bash
npm install
```

## Development

Compile Sass once:

```bash
npm run build
```

Watch Sass files during development:

```bash
npm run watch
```

Open the project with Live Server from VS Code.

Recommended local URL:

```text
http://localhost:5500/
```

## JavaScript Features

The project includes several JavaScript features:

- Header and footer loading with jQuery.
- Featured shows carousel on the homepage.
- Dynamic show cards generated from `assets/data/spectacles.json`.
- Filters on the programming page:
  - by show type
  - by date
  - by availability
- Sorting options:
  - date ascending
  - date descending
  - price ascending
  - price descending
- Progress bars showing sold seats out of 120.
- Visual status for each show:
  - available
  - few seats left
  - sold out

## JSON Data

Show data is stored in:

```text
assets/data/spectacles.json
```

Each show contains:

- title
- type
- date
- time
- duration
- price
- total seats
- sold seats
- artist
- image

## Responsive Design

The website is designed for:

- desktop screens
- tablets
- mobile devices

The layout adapts through Sass media queries.  
The programming cards display in multiple columns on desktop and in one column on mobile.

## Accessibility Notes

Accessibility was considered through:

- semantic HTML structure
- alternative text on images
- ARIA labels on navigation elements
- visible text hierarchy
- responsive typography
- contrast based on the provided color palette

Further RGAA testing should be completed before final delivery.

## Design Guidelines

The project follows the client color palette:

- Burgundy: `#6B1D3A`
- Gold: `#D4A843`
- Anthracite: `#2A2D34`
- Cream: `#F5F0E8`

Typography:

- Headings: Playfair Display
- Body text: Inter

## Validation and Testing

Before final delivery, the following checks should be completed:

- HTML validation with W3C Validator
- CSS validation
- JavaScript linting with ESLint
- Responsive screenshots on desktop, tablet, and mobile
- Browser testing on Chrome and at least one other browser
- Accessibility checks for contrast, keyboard navigation, and screen reader structure

Run project checks:

```bash
npm run check
```

## Deployment

The project can be deployed using:

- GitHub Pages
- A secure hosting provider with HTTPS
- SFTP deployment if required by the client

Deployment steps:

1. Build the Sass file:

```bash
npm run build
```

2. Upload the project files to the hosting server.
3. Check that all pages, assets, styles, and scripts load correctly.
4. Test the deployed website on desktop and mobile.

## Author

Faten  
DWWM Front-End Assessment - 2026
