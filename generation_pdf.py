from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def page_image_pdf(pdf, data):
    page_width, page_height = A4

    # Taille originale de l'image
    img_width, img_height = data["size_image"]

    # Calcul du facteur pour garder le ratio
    scale_w = page_width / img_width
    scale_h = page_height / img_height
    scale = min(scale_w, scale_h)  # ne dépasse pas la page

    # Nouvelle taille
    new_width = img_width * scale
    new_height = img_height * scale

    # Centrer l'image
    x = (page_width - new_width) / 2
    y = (page_height - new_height) / 2

    # Dessiner l'image
    pdf.drawImage(data["image"], x, y, width=new_width, height=new_height)

    pdf.showPage()  # passer à la page suivante


def palette(c, data, page_width, page_height):
    # Mise en page
    margin = 50
    cell_size = 40
    padding = 20
    text_offset = 12

    # Colonnes calculées automatiquement
    cols = int((page_width - 2 * margin) // (cell_size + padding))

    x_start = margin
    y_start = page_height - margin -100

    x = x_start
    y = y_start

    c.setFont("Helvetica", 7)
    for i in range (len(data['palette'])):
        (r, g, b, m) = data['palette'][i]
        # Nouvelle page si on descend trop bas
        if y < margin + cell_size:
            c.showPage()
            c.setFont("Helvetica", 7)
            x = x_start
            y = y_start

        # Dessin du carré
        c.setFillColorRGB(r / 255, g / 255, b / 255)
        c.rect(x, y, cell_size, cell_size, fill=1, stroke=1)

        # Texte RGB
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(
            x + cell_size / 2,
            y - text_offset,
            f"RGB({r},{g},{b})"
        )

        # Déplacement
        x += cell_size + padding

        # Retour à la ligne
        if x + cell_size > page_width - margin:
            x = x_start
            y -= cell_size + padding + text_offset

def create_pdf(data):
    # Créer le PDF
    nom = str(input("Donner une nom à votre projet : "))

    c = canvas.Canvas((nom +".pdf"), pagesize=A4)
    width, height = A4

    # Titre
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, nom)

    # Infos
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Taille du pixel art : {data['size_image_pixel']}")

    # Palette
    palette(c, data, width, height)

    # Image
    c.showPage()
    page_image_pdf(c, data)

    # Finaliser
    c.save()