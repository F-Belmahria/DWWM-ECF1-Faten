from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
    PageBreak,
)


ROOT = Path(r"C:\Users\faten\Documents\GitHub\DWWM-ECF1-Faten")
IMG_DIR = ROOT / "tmp" / "photographie33_images"
OUT_DIR = ROOT / "output" / "pdf"
OUT_PDF = OUT_DIR / "Validation_travail_LA_Photographie33_Faten_Belmahria.pdf"

FONT_DIR = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("Calibri", str(FONT_DIR / "calibri.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Bold", str(FONT_DIR / "calibrib.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Italic", str(FONT_DIR / "calibrii.ttf")))

BLUE = colors.HexColor("#2E74B5")
DARK_BLUE = colors.HexColor("#1F4D78")
LIGHT_GRAY = colors.HexColor("#F2F4F7")
GRAY = colors.HexColor("#555555")


def para(text, style):
    return Paragraph(text.replace("&", "&amp;"), style)


def table(data, widths=None, header=True):
    if widths is None:
        widths = [1.8 * inch, 2.35 * inch, 2.35 * inch] if len(data[0]) == 3 else [1.9 * inch, 4.5 * inch]
    t = Table(data, colWidths=widths, hAlign="CENTER", repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("FONTNAME", (0, 0), (-1, -1), "Calibri"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.2),
    ]
    if header:
        style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), LIGHT_GRAY),
            ("TEXTCOLOR", (0, 0), (-1, 0), DARK_BLUE),
            ("FONTNAME", (0, 0), (-1, 0), "Calibri-Bold"),
        ])
    t.setStyle(TableStyle(style))
    return t


def code_block(lines):
    text = "<br/>".join(line.replace("<", "&lt;").replace(">", "&gt;") for line in lines)
    t = Table([[Paragraph(text, STYLES["code"])]], colWidths=[6.3 * inch], hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#D0D0D0")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F7F7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def image_with_caption(filename, caption, width):
    img_path = IMG_DIR / filename
    img = Image(str(img_path), width=width * inch, height=width * inch * 0.62)
    img._restrictSize(width * inch, 4.4 * inch)
    return KeepTogether([
        img,
        Paragraph(caption, STYLES["caption"]),
        Spacer(1, 0.08 * inch),
    ])


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Calibri", 9)
    canvas.setFillColor(GRAY)
    canvas.drawRightString(7.5 * inch, 0.55 * inch, f"Page {doc.page}")
    canvas.restoreState()


OUT_DIR.mkdir(parents=True, exist_ok=True)
styles = getSampleStyleSheet()
STYLES = {
    "title": ParagraphStyle("title", parent=styles["Title"], fontName="Calibri-Bold", fontSize=22, leading=26, alignment=TA_CENTER, textColor=DARK_BLUE, spaceAfter=4),
    "subtitle": ParagraphStyle("subtitle", parent=styles["Normal"], fontName="Calibri-Italic", fontSize=12, leading=15, alignment=TA_CENTER, textColor=GRAY, spaceAfter=16),
    "h1": ParagraphStyle("h1", parent=styles["Heading1"], fontName="Calibri-Bold", fontSize=16, leading=20, textColor=BLUE, spaceBefore=14, spaceAfter=7),
    "h2": ParagraphStyle("h2", parent=styles["Heading2"], fontName="Calibri-Bold", fontSize=13, leading=16, textColor=BLUE, spaceBefore=10, spaceAfter=5),
    "body": ParagraphStyle("body", parent=styles["Normal"], fontName="Calibri", fontSize=10.6, leading=13.3, spaceAfter=6, alignment=TA_LEFT),
    "caption": ParagraphStyle("caption", parent=styles["Normal"], fontName="Calibri-Italic", fontSize=8.8, leading=11, textColor=GRAY, alignment=TA_CENTER, spaceAfter=6),
    "code": ParagraphStyle("code", parent=styles["Code"], fontName="Courier", fontSize=8, leading=10, textColor=colors.HexColor("#222222")),
}

story = [
    para("Validation du travail réalisé", STYLES["title"]),
    para("Projet LA Photographie33 - site vitrine d'un photographe professionnel", STYLES["subtitle"]),
    table([
        ["Élément", "Détail"],
        ["Candidate", "BELMAHRIA Faten"],
        ["Titre visé", "Développeur Web et Web Mobile (DWWM)"],
        ["Activité-type", "Développer la partie front-end d'une application web"],
        ["Projet", "LA Photographie33 - site vitrine d'un photographe professionnel"],
        ["Organisation", "Conception Figma et développement réalisés en équipe"],
        ["Période attestée", "Juin 2026 - contributions GitHub du 5 au 9 juin 2026"],
        ["Technologies", "Figma, HTML5, SCSS, Bootstrap 5, Git et GitHub"],
    ], widths=[1.65 * inch, 4.75 * inch]),
    Spacer(1, 0.12 * inch),
    para("Fil conducteur", STYLES["h1"]),
    para("J'ai participé avec l'équipe à la conception de l'expérience utilisateur et des écrans responsive. Pendant le développement, j'ai notamment pris en charge des éléments identifiables du site : l'illustration de contact et la page Blog.", STYLES["body"]),
    para("Compétences mobilisées", STYLES["h2"]),
    table([
        ["Compétence", "Travail réalisé", "Apport professionnel"],
        ["UX/UI", "Organisation des contenus et maquettes responsive", "Parcours clair et cohérent"],
        ["Front-end", "HTML sémantique, SCSS et Bootstrap", "Interfaces statiques structurées"],
        ["Responsive", "Breakpoints, grille et adaptation des images", "Utilisation multi-écrans"],
        ["Accessibilité", "Alternatives textuelles et attributs ARIA", "Interface plus inclusive"],
        ["Collaboration", "Branche personnelle, commits et pull requests", "Travail collectif traçable"],
    ]),
    para("1. Contexte du projet", STYLES["h1"]),
    para("Dans le cadre de la formation DWWM, le projet consistait à concevoir puis à réaliser un site vitrine pour une activité de photographie professionnelle. Le site devait présenter l'univers du photographe, ses prestations, ses galeries et ses contenus éditoriaux, tout en facilitant la prise de contact et la réservation d'une séance.", STYLES["body"]),
    para("La conception a été menée en équipe. Nous avons étudié les contenus attendus, organisé les pages et construit les maquettes sur Figma. Le développement a ensuite été réalisé par le même groupe à partir d'un dépôt GitHub commun.", STYLES["body"]),
    para("Objectifs fonctionnels", STYLES["h2"]),
    table([
        ["Objectif", "Ce que cela apporte", "Exemple dans le projet"],
        ["Présenter les prestations", "Compréhension rapide de l'offre", "Mariage, maternité, portrait, sport, animalier et événements"],
        ["Valoriser les photographies", "Hiérarchie visuelle sobre", "Grands formats d'image et espaces aérés"],
        ["Adapter l'interface", "Navigation fluide sur ordinateur et mobile", "Maquettes desktop et mobile, règles responsive"],
        ["Créer des appels à l'action", "Faciliter la réservation", "Boutons vers contact, galerie ou blog"],
    ]),
    para("2. Conception en équipe", STYLES["h1"]),
    para("Avec l'équipe, j'ai participé à la définition des grandes zones de contenu et du parcours utilisateur. Cette étape nous a permis de hiérarchiser l'information avant de travailler les détails graphiques. Nous avons ensuite décliné les écrans dans Figma en distinguant les formats desktop et mobile.", STYLES["body"]),
    image_with_caption("wireframes.png", "Wireframes des principales pages et déclinaisons desktop/mobile réalisés sur Figma.", 5.8),
    para("Maquettage responsive de la page d'accueil", STYLES["h2"]),
    para("Dans ce projet réalisé en équipe, j'ai pris en charge la conception de la page d'accueil sur Figma, dans ses versions desktop et mobile. J'ai organisé les sections : bannière principale, présentation du photographe, prestations, témoignages, tarifs, contact et pied de page.", STYLES["body"]),
    image_with_caption("maquette_accueil.png", "Maquettes desktop et mobile de la page d'accueil réalisées sur Figma.", 3.5),
    para("Prototypage et interactions", STYLES["h2"]),
    para("Après les maquettes, j'ai réalisé le prototypage interactif sur Figma. J'ai relié les boutons, les éléments de navigation et les appels à l'action aux écrans correspondants afin de simuler le parcours utilisateur avant le développement.", STYLES["body"]),
    image_with_caption("prototype_interactions.png", "Création des interactions et du parcours utilisateur dans le prototype Figma.", 5.6),
    PageBreak(),
    para("Direction artistique", STYLES["h2"]),
    para("L'identité visuelle repose sur une palette douce et chaleureuse, adaptée à l'univers de la photographie de famille et d'événement. Le blanc structure les espaces, les tons rosés servent d'accent et les teintes brunes apportent du contraste.", STYLES["body"]),
    image_with_caption("palette_couleurs.png", "Palette de couleurs utilisée pour l'identité visuelle du site.", 3.2),
    para("Playfair Display est utilisée pour les titres principaux afin de donner une dimension éditoriale. Montserrat améliore la lisibilité des textes courants et des éléments d'interface. Une police manuscrite, Miama, est employée ponctuellement pour renforcer la personnalité de certains titres.", STYLES["body"]),
    para("3. Passage de la maquette au site web", STYLES["h1"]),
    para("Après la phase de conception, nous avons poursuivi le développement du site. Le dépôt commun a été structuré autour de pages HTML, de feuilles de style CSS générées depuis SCSS et d'un dossier d'images et de polices. Bootstrap a été utilisé pour accélérer la mise en page responsive et fournir des composants d'interface fiables.", STYLES["body"]),
    table([
        ["Outil", "Contribution personnelle", "Apport professionnel"],
        ["HTML5", "Structure sémantique des pages et des contenus", "Lisibilité, accessibilité et référencement"],
        ["SCSS", "Styles modulaires et classes structurées", "Maintenance et réutilisation"],
        ["Bootstrap 5", "Grille responsive, utilitaires et composant collapse", "Adaptation rapide aux écrans"],
        ["Git/GitHub", "Branche faten-modifications et pull requests", "Traçabilité et intégration collective"],
        ["Figma", "Maquettes desktop et mobile", "Référence visuelle partagée"],
    ]),
    para("4. Contribution personnelle : illustration de contact", STYLES["h1"]),
    para("L'illustration de contact constitue un appel à l'action placé à un moment stratégique du parcours. Elle associe une image, un titre, un texte court et un bouton de réservation.", STYLES["body"]),
    code_block([
        '<div class="illustration-contact container-fluid p-0">',
        '  <div class="illustration-contact__content ...">',
        '    <h2>Prêt à capturer vos plus beaux instants ?</h2>',
        '    <a class="btn illustration-contact__button">Réserver une séance</a>',
        '  </div>',
        '</div>',
    ]),
    para("J'ai organisé les styles avec des classes de type BEM. Sous 768 px, l'image passe en arrière-plan sur mobile afin de préserver la composition.", STYLES["body"]),
    code_block([
        "@media (max-width: 767.98px) {",
        "  .illustration-contact { background-size: cover; }",
        "  .illustration-contact__card { width: min(312px, calc(100% - 32px)); }",
        "}",
    ]),
    para("Preuve GitHub : création des fichiers HTML et SCSS le 5 juin 2026, ajout de l'image contact__image.png, puis corrections successives sur la branche faten-modifications.", STYLES["body"]),
    para("5. Contribution personnelle : page Blog", STYLES["h1"]),
    para("La page Blog devait présenter les contenus éditoriaux du photographe et permettre à l'utilisateur de retrouver rapidement un article. J'ai développé le hero, la navigation par catégories, les cartes d'articles et la barre latérale.", STYLES["body"]),
    table([
        ["Bloc", "Réalisation", "Objectif"],
        ["Hero", "Image, voile de contraste, titre et introduction", "Entrée visuelle claire"],
        ["Catégories", "Navigation desktop et filtres repliables sur mobile", "Parcours adapté au terminal"],
        ["Articles", "Image, catégorie, titre, résumé, date et lien", "Lecture rapide des contenus"],
        ["Sidebar", "Recherche, catégories et articles populaires", "Accès direct aux contenus utiles"],
    ]),
    para("Sur ordinateur, la liste d'articles occupe neuf colonnes et la barre latérale trois colonnes. Sur les écrans plus étroits, les blocs passent en pleine largeur. La navigation desktop est masquée sous 768 px et remplacée par un bouton de filtres utilisant le composant collapse de Bootstrap.", STYLES["body"]),
    code_block([
        '<section class="col-12 col-lg-9">...</section>',
        '<aside class="col-12 col-lg-3">...</aside>',
        '<button data-bs-toggle="collapse" data-bs-target="#mobileFilters">',
        "  Afficher les filtres",
        "</button>",
    ]),
    para("Preuve GitHub : création de la page Blog le 8 juin 2026, enrichissement progressif de son contenu et de ses styles, puis intégration par pull requests.", STYLES["body"]),
    para("6. Qualité de l'interface", STYLES["h1"]),
    para("Responsive design : les règles SCSS utilisent plusieurs points de rupture : 991,98 px pour les tablettes, 767,98 px pour les mobiles et 399,98 px pour les très petits écrans.", STYLES["body"]),
    para("Accessibilité : les images de contenu disposent d'un attribut alt descriptif. Les zones de navigation sont nommées avec aria-label. Le bouton de filtres renseigne aria-expanded et aria-controls.", STYLES["body"]),
    para("Maintenabilité : la convention de nommage des classes permet de repérer rapidement le bloc, l'élément et son rôle. Les styles sont regroupés par composant et les valeurs responsive sont centralisées dans les media queries.", STYLES["body"]),
    para("7. Collaboration et traçabilité", STYLES["h1"]),
    para("Le projet a été suivi dans le dépôt Juanrojasdc/projet-site-photo. J'ai travaillé sur la branche faten-modifications afin d'isoler mes changements et d'éviter de modifier directement la branche principale.", STYLES["body"]),
    table([
        ["Date", "Contribution personnelle", "Apport"],
        ["5 juin", "Création de l'illustration Contact en HTML et SCSS", "Premier composant personnel"],
        ["5 juin", "Ajout de contact__image.png et corrections responsive", "Amélioration visuelle"],
        ["8 juin", "Création de la page Le Blog et de ses styles", "Nouvelle page complète"],
        ["8-9 juin", "Corrections HTML/SCSS et enrichissement de la page", "Itérations et stabilisation"],
        ["PR #2 à #5", "Propositions d'intégration depuis faten-modifications", "Collaboration traçable"],
    ]),
    para("Dépôt de référence : github.com/Juanrojasdc/projet-site-photo", STYLES["body"]),
    para("8. Réponses synthétiques pour validation", STYLES["h1"]),
    para("Tâches réalisées et conditions", STYLES["h2"]),
    para("J'ai participé avec mon équipe à la conception des maquettes responsive d'un site de photographie dans Figma. Ma contribution identifiable a porté sur l'illustration de contact et sur la page Blog, développées en HTML5, SCSS et Bootstrap, puis intégrées au moyen de Git et GitHub.", STYLES["body"]),
    para("Moyens utilisés", STYLES["h2"]),
    para("Figma pour la conception des écrans ; HTML5 pour la structure ; SCSS et CSS3 pour les styles ; Bootstrap 5 et Bootstrap Icons pour la grille, les utilitaires et les composants responsive ; Git et GitHub pour la branche personnelle, les commits et les pull requests.", STYLES["body"]),
    para("Avec qui avez-vous travaillé ?", STYLES["h2"]),
    para("J'ai participé, avec mon équipe de trois personnes, à la conception des maquettes responsive du site LA Photographie33 sur Figma, puis au développement collectif du site.", STYLES["body"]),
    para("Contexte", STYLES["h2"]),
    table([
        ["Élément", "Détail"],
        ["Organisme", "AFPA Bègles"],
        ["Période d'exercice", "Du 23/03/2026 au 18/12/2026"],
        ["Cadre", "Projet pédagogique réalisé pendant la formation Développeur Web et Web Mobile"],
    ], widths=[1.65 * inch, 4.75 * inch]),
    para("Axes d'amélioration", STYLES["h2"]),
    table([
        ["Axe", "Action prévue", "Intérêt"],
        ["Validation", "Renforcer les tests automatisés et les contrôles HTML/CSS", "Fiabiliser l'intégration"],
        ["Performance", "Optimiser davantage les images et mesurer les performances", "Améliorer le chargement"],
        ["Documentation", "Documenter les composants partagés et centraliser les variables SCSS", "Faciliter la maintenance"],
        ["Accessibilité", "Approfondir les tests clavier et lecteur d'écran", "Rendre l'interface plus inclusive"],
    ]),
    para("Conclusion", STYLES["h1"]),
    para("Cette réalisation confirme ma capacité à concevoir une interface, à développer des pages responsive et à collaborer dans un projet versionné. Le travail réalisé sur LA Photographie33 montre une contribution identifiable, vérifiable et reliée aux compétences front-end attendues dans le titre DWWM.", STYLES["body"]),
]

doc = SimpleDocTemplate(
    str(OUT_PDF),
    pagesize=letter,
    rightMargin=1 * inch,
    leftMargin=1 * inch,
    topMargin=1 * inch,
    bottomMargin=0.8 * inch,
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(OUT_PDF)
