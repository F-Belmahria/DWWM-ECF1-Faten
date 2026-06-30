from pathlib import Path
from html import escape
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


ROOT = Path(r"C:\MAMP\htdocs\blog")
OUT = Path(r"C:\Users\faten\Documents\GitHub\DWWM-ECF1-Faten\output\pdf\resume_blog_dwwm.pdf")

ARIAL = r"C:\Windows\Fonts\arial.ttf"
ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
CONSOLAS = r"C:\Windows\Fonts\consola.ttf"

pdfmetrics.registerFont(TTFont("Arial", ARIAL))
pdfmetrics.registerFont(TTFont("Arial-Bold", ARIAL_BOLD))
pdfmetrics.registerFont(TTFont("Consolas", CONSOLAS))


PALETTE = {
    "blue": colors.HexColor("#1f5fbf"),
    "green": colors.HexColor("#1f7a3f"),
    "purple": colors.HexColor("#6f3cc3"),
    "orange": colors.HexColor("#c45a10"),
    "gray": colors.HexColor("#697386"),
    "dark": colors.HexColor("#172033"),
    "light_blue": colors.HexColor("#eaf2ff"),
    "light_green": colors.HexColor("#eaf8ef"),
    "light_purple": colors.HexColor("#f2edff"),
    "light_orange": colors.HexColor("#fff1e6"),
}


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleMain",
    fontName="Arial-Bold",
    fontSize=24,
    leading=30,
    textColor=PALETTE["dark"],
    alignment=TA_CENTER,
    spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="H1",
    fontName="Arial-Bold",
    fontSize=18,
    leading=23,
    textColor=PALETTE["dark"],
    spaceBefore=8,
    spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="H2",
    fontName="Arial-Bold",
    fontSize=13,
    leading=17,
    textColor=PALETTE["dark"],
    spaceBefore=8,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="Body",
    fontName="Arial",
    fontSize=10.5,
    leading=15,
    textColor=colors.HexColor("#253044"),
    spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="CodeLine",
    fontName="Consolas",
    fontSize=7.6,
    leading=9.3,
    textColor=PALETTE["dark"],
))
styles.add(ParagraphStyle(
    name="Small",
    fontName="Arial",
    fontSize=9,
    leading=12,
    textColor=colors.HexColor("#4b5563"),
))


def line_color(line: str):
    s = line.strip()
    if not s:
        return colors.HexColor("#253044")
    if s.startswith("//"):
        return PALETTE["gray"]
    if any(k in s for k in ["define(", "new PDO", "setAttribute", "$dsn", "DB_HOST", "DB_NAME", "DB_USER", "DB_PASS"]):
        return PALETTE["blue"]
    if any(k in s for k in ["SELECT", "query(", "fetchAll", "fetch()", "$articles", "$sql"]):
        return PALETTE["green"]
    if any(k in s for k in ["intval", "prepare(", "execute(", "header(", "exit", "$_GET"]):
        return PALETTE["orange"]
    if any(k in s for k in ["htmlspecialchars", "nl2br", "<", ">", "Bootstrap", "class=", "href=", "<?= "]):
        return PALETTE["purple"]
    return colors.HexColor("#253044")


def add_chip(text, bg, fg):
    return Table(
        [[Paragraph(f"<b>{escape(text)}</b>", ParagraphStyle(
            name="ChipText",
            parent=styles["Small"],
            fontName="Arial-Bold",
            textColor=fg,
            leading=11,
        ))]],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("BOX", (0, 0), (-1, -1), 0.6, fg),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ],
    )


def explanation_box(title, text, bg, border):
    return Table(
        [[
            Paragraph(f"<b>{escape(title)}</b><br/>{escape(text)}", styles["Body"])
        ]],
        colWidths=[16.3 * cm],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("BOX", (0, 0), (-1, -1), 0.8, border),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ],
    )


def code_table(code: str):
    rows = []
    for i, line in enumerate(code.splitlines(), start=1):
        chunks = textwrap.wrap(line, width=92, replace_whitespace=False, drop_whitespace=False) or [""]
        for j, chunk in enumerate(chunks):
            number = f"{i:02d}" if j == 0 else "  "
            color = line_color(line)
            rows.append([
                Paragraph(f'<font color="#7b8794">{number}</font>', styles["CodeLine"]),
                Paragraph(f'<font color="{color.hexval()}">{escape(chunk)}</font>', styles["CodeLine"]),
            ])
    table = Table(rows, colWidths=[0.8 * cm, 15.5 * cm], repeatRows=0)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7f9fc")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#d4dce8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(1.6 * cm, 1.0 * cm, "TP Mon Premier Blog - resume du code")
    canvas.drawRightString(19.4 * cm, 1.0 * cm, f"Page {doc.page}")
    canvas.restoreState()


def file_section(story, filename, purpose, boxes):
    code = (ROOT / filename).read_text(encoding="utf-8")
    story.append(Paragraph(filename, styles["H1"]))
    story.append(Paragraph(purpose, styles["Body"]))
    for title, text, bg, border in boxes:
        story.append(explanation_box(title, text, bg, border))
        story.append(Spacer(1, 6))
    story.append(Paragraph("Code complet", styles["H2"]))
    story.append(code_table(code))


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )
    story = []

    story.append(Paragraph("Resume du TP - Mon Premier Blog", styles["TitleMain"]))
    story.append(Paragraph(
        "Ce PDF explique les trois pages du projet PHP/MySQL. Les codes sont ceux du TP, avec les trous remplis seulement.",
        styles["Body"],
    ))
    legend = Table(
        [[
            add_chip("Bleu = connexion/base", PALETTE["light_blue"], PALETTE["blue"]),
            add_chip("Vert = requetes SQL", PALETTE["light_green"], PALETTE["green"]),
        ], [
            add_chip("Violet = HTML/affichage", PALETTE["light_purple"], PALETTE["purple"]),
            add_chip("Orange = securite/URL", PALETTE["light_orange"], PALETTE["orange"]),
        ]],
        colWidths=[8.0 * cm, 8.0 * cm],
        style=[("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4)],
    )
    story.append(legend)
    story.append(Spacer(1, 10))
    story.append(explanation_box(
        "Vue d'ensemble",
        "connexion.php ouvre la connexion PDO. index.php lit tous les articles et les affiche en cartes Bootstrap. article.php recupere un id dans l'URL, cherche un seul article, puis affiche son contenu complet.",
        colors.HexColor("#eef2f7"),
        colors.HexColor("#94a3b8"),
    ))
    story.append(PageBreak())

    file_section(story, "connexion.php", "Cette page ne s'affiche pas directement dans le blog. Elle prepare seulement la variable $pdo, utilisee ensuite par index.php et article.php.", [
        ("Configuration", "DB_HOST, DB_NAME, DB_USER et DB_PASS indiquent a PHP ou trouver la base MySQL. Pour MAMP, le mot de passe utilise ici est root.", PALETTE["light_blue"], PALETTE["blue"]),
        ("Connexion PDO", "new PDO(...) cree la connexion. Les setAttribute demandent a PDO d'afficher les erreurs et de renvoyer les resultats sous forme de tableaux associatifs.", PALETTE["light_blue"], PALETTE["blue"]),
    ])
    story.append(PageBreak())

    file_section(story, "index.php", "C'est la page d'accueil du blog. Elle recupere les articles dans la base et les affiche un par un.", [
        ("require 'connexion.php'", "Cette ligne importe la connexion. Sans elle, la variable $pdo n'existe pas et PHP ne peut pas parler a MySQL.", PALETTE["light_blue"], PALETTE["blue"]),
        ("SELECT + query + fetchAll", "La requete SELECT recupere tous les articles. ORDER BY date_publication DESC les trie du plus recent au plus ancien. fetchAll recupere toutes les lignes.", PALETTE["light_green"], PALETTE["green"]),
        ("foreach", "La boucle foreach parcourt le tableau $articles. A chaque tour, elle affiche une carte Bootstrap avec le titre, l'auteur, la date, un extrait et le bouton Lire la suite.", PALETTE["light_purple"], PALETTE["purple"]),
    ])
    story.append(PageBreak())

    file_section(story, "article.php", "Cette page affiche un seul article complet. Elle utilise l'id envoye dans l'URL, par exemple article.php?id=5.", [
        ("Recuperation de l'id", "intval($_GET['id'] ?? 0) transforme l'id de l'URL en nombre. Si l'id est absent ou invalide, la page redirige vers index.php.", PALETTE["light_orange"], PALETTE["orange"]),
        ("prepare + execute", "Comme l'id vient de l'utilisateur, on utilise une requete preparee. C'est plus securise contre les injections SQL.", PALETTE["light_orange"], PALETTE["orange"]),
        ("fetch", "fetch recupere une seule ligne, car un id correspond a un seul article. Si aucun article n'est trouve, on retourne a l'accueil.", PALETTE["light_green"], PALETTE["green"]),
        ("Affichage", "htmlspecialchars protege l'affichage du texte. nl2br garde les retours a la ligne dans le contenu de l'article.", PALETTE["light_purple"], PALETTE["purple"]),
    ])

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


if __name__ == "__main__":
    build()
