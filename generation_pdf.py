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
    global nuancier_hama
    # Mise en page
    margin = 50
    cell_size = 40
    padding = 50  # Espace horizontal augmenté entre chaque carré
    text_spacing = 11  # Espace vertical entre les lignes de texte

    # On fixe le nombre de colonnes à 4 pour bien aérer la ligne
    cols_par_ligne = 4

    x_start = margin
    x = x_start
    y = page_height - margin - 100

    c.setFont("Helvetica", 7)

    compteur_ligne = 0
    for i in range(len(data['palette'])):
        (r, g, b) = data['palette'][i]

        # Nouvelle page si on descend trop bas (on laisse de la marge pour le texte)
        if y < margin + cell_size + 50:
            c.showPage()
            c.setFont("Helvetica", 7)
            x = x_start
            y = page_height - margin - 100
            compteur_ligne = 0

        # Dessin du carré de couleur
        c.setFillColorRGB(r / 255, g / 255, b / 255)
        c.rect(x, y, cell_size, cell_size, fill=1, stroke=1)

        # Récupération des infos depuis le dictionnaire
        info = nuancier_hama.get((r, g, b), {"nom": "Inconnu", "numero": ""})
        nom = info["nom"]
        numero = info["numero"]

        # Préparation des deux lignes de texte
        ligne_nom = f"N°{numero} : {nom}"
        ligne_rgb = f"RGB({r}, {g}, {b})"

        c.setFillColorRGB(0, 0, 0)

        # Affichage du nom et numéro sous le carré
        c.drawCentredString(
            x + cell_size / 2,
            y - text_spacing,
            ligne_nom
        )

        # Affichage du code RGB en dessous
        c.drawCentredString(
            x + cell_size / 2,
            y - (text_spacing * 2.3),
            ligne_rgb
        )

        # Passage à la colonne suivante avec un grand espacement
        compteur_ligne += 1
        x += cell_size + padding

        # Si on a atteint le nombre max de colonnes par ligne, on retourne à la ligne
        if compteur_ligne >= cols_par_ligne:
            x = x_start
            y -= cell_size + padding + 15  # Grand espace vertical pour la ligne suivante
            compteur_ligne = 0

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

nuancier_hama = {
    (255, 255, 255): {"nom": "Blanc", "numero": 1},
    (255, 253, 230): {"nom": "Crème", "numero": 2},
    (255, 220, 0): {"nom": "Jaune", "numero": 3},
    (255, 130, 0): {"nom": "Orange", "numero": 4},
    (220, 20, 60): {"nom": "Rouge", "numero": 5},
    (255, 150, 180): {"nom": "Rose", "numero": 6},
    (110, 40, 140): {"nom": "Violet", "numero": 7},
    (0, 80, 180): {"nom": "Bleu", "numero": 8},
    (100, 180, 240): {"nom": "Bleu clair", "numero": 9},
    (0, 140, 60): {"nom": "Vert", "numero": 10},
    (120, 200, 80): {"nom": "Vert clair", "numero": 11},
    (120, 60, 20): {"nom": "Marron", "numero": 12},
    (240, 245, 250): {"nom": "Transparent", "numero": 13},
    (255, 240, 150): {"nom": "Jaune pastel", "numero": 14},
    (100, 110, 50): {"nom": "Olive", "numero": 15},
    (200, 160, 210): {"nom": "Lilas", "numero": 16},
    (128, 128, 128): {"nom": "Gris", "numero": 17},
    (30, 30, 30): {"nom": "Noir", "numero": 18},
    (245, 245, 245): {"nom": "Clair transparent", "numero": 19},
    (230, 80, 90): {"nom": "Rouge transparent", "numero": 20},
    (80, 150, 220): {"nom": "Bleu transparent", "numero": 21},
    (80, 180, 110): {"nom": "Vert transparent", "numero": 22},
    (150, 100, 180): {"nom": "Violet transparent", "numero": 24},
    (255, 210, 190): {"nom": "Rose chair / Peau", "numero": 26},
    (210, 170, 130): {"nom": "Beige", "numero": 27},
    (0, 80, 40): {"nom": "Vert foncé", "numero": 28},
    (120, 20, 40): {"nom": "Bordeaux / Rouge foncé", "numero": 29},
    (130, 220, 240): {"nom": "Cyan / Bleu glacier", "numero": 30},
    (64, 224, 208): {"nom": "Turquoise", "numero": 31},
    (220, 20, 120): {"nom": "Fuchsia", "numero": 32},
    (210, 160, 40): {"nom": "Jaune moutarde / Doré", "numero": 34},
    (255, 180, 120): {"nom": "Melon / Orange pastel", "numero": 35},
    (150, 230, 200): {"nom": "Vert menthe", "numero": 36},
    (140, 100, 160): {"nom": "Lilas foncé", "numero": 37},
    (90, 100, 110): {"nom": "Gris métal", "numero": 38},
    (255, 250, 200): {"nom": "Pastel jaune", "numero": 43},
    (255, 210, 230): {"nom": "Pastel rose", "numero": 44},
    (200, 230, 255): {"nom": "Pastel bleu", "numero": 45},
    (200, 240, 210): {"nom": "Pastel vert", "numero": 46},
    (230, 210, 240): {"nom": "Pastel lila", "numero": 47},
    (180, 140, 200): {"nom": "Pastel violet", "numero": 48},
    (50, 130, 200): {"nom": "Azure", "numero": 49},
    (50, 255, 50): {"nom": "Vert fluo", "numero": 55},
    (255, 20, 147): {"nom": "Rose fluo", "numero": 56},
    (180, 120, 80): {"nom": "Brun clair", "numero": 60},
    (140, 70, 50): {"nom": "Brun rouge", "numero": 61},
    (110, 90, 80): {"nom": "Taupe / Gris-brun", "numero": 62},
    (190, 190, 190): {"nom": "Gris clair", "numero": 63},
    (80, 80, 80): {"nom": "Gris foncé", "numero": 64},
    (255, 255, 0): {"nom": "Jaune fluo", "numero": 70},
    (255, 100, 0): {"nom": "Orange fluo", "numero": 71},
    (170, 220, 0): {"nom": "Vert pomme", "numero": 72},
    (10, 30, 80): {"nom": "Bleu nuit", "numero": 73},
    (255, 200, 150): {"nom": "Abricot", "numero": 74},
    (180, 40, 90): {"nom": "Framboise", "numero": 75},
    (255, 170, 130): {"nom": "Pêche", "numero": 76},
    (40, 100, 60): {"nom": "Vert forêt", "numero": 77},
    (80, 40, 20): {"nom": "Chocolat", "numero": 78},
    (160, 100, 50): {"nom": "Caramel", "numero": 79},
    (20, 90, 70): {"nom": "Vert pin", "numero": 82},
    (0, 100, 120): {"nom": "Bleu pétrole", "numero": 83},
    (210, 180, 220): {"nom": "Lilas tendre", "numero": 84},
    (220, 180, 80): {"nom": "Or pailleté / Jaune ocre", "numero": 95},
    (180, 180, 190): {"nom": "Argent pailleté", "numero": 96},
    (150, 150, 150): {"nom": "Multicolore / Mix", "numero": 97},
    (240, 240, 245): {"nom": "Nacré / Perlé", "numero": 98},
    (180, 220, 240): {"nom": "Bleu glacier / Pâle", "numero": 101},
    (180, 240, 210): {"nom": "Vert d'eau / Menthe clair", "numero": 102},
    (255, 200, 210): {"nom": "Rose poudré", "numero": 103},
    (255, 240, 180): {"nom": "Jaune vanille", "numero": 104},
    (240, 220, 200): {"nom": "Beige clair / Nude", "numero": 105},
    (210, 210, 210): {"nom": "Gris perle", "numero": 106},
    (170, 150, 140): {"nom": "Taupe clair", "numero": 107},
    (190, 140, 130): {"nom": "Brun rosé", "numero": 108},
    (200, 100, 70): {"nom": "Terracotta / Ocre rouge", "numero": 109},
    (130, 160, 130): {"nom": "Vert sauge", "numero": 110},
    (100, 130, 170): {"nom": "Bleu jean", "numero": 111},
    (170, 150, 200): {"nom": "Lavande", "numero": 112},
    (90, 40, 70): {"nom": "Prune", "numero": 113},
    (60, 60, 70): {"nom": "Gris anthracite", "numero": 114},
    (90, 100, 70): {"nom": "Vert kaki", "numero": 115},
    (255, 120, 100): {"nom": "Corail", "numero": 117},
    (230, 60, 140): {"nom": "Rose fuchsia soutenu", "numero": 118},
    (50, 110, 160): {"nom": "Bleu arctique", "numero": 119},
    (0, 120, 90): {"nom": "Vert émeraude", "numero": 120},
    (60, 30, 20): {"nom": "Brun foncé / Espresso", "numero": 121},
    (245, 240, 230): {"nom": "Blanc cassé / Lin", "numero": 122},
}