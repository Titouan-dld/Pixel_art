from PIL import Image
import json
from generation_pdf import create_pdf
import math
import colorsys

pixel_art = Image.open("discovery_pixel_art.png")

def rgb_to_hsv(c):
    list = [x/255 for x in c]
    h, s, v = colorsys.rgb_to_hsv(list[0], list[1], list[2])
    return h, s, v

def luminosite(c):
    r, g, b, g = c
    return 0.299*r + 0.587*g + 0.114*b  # pondération perceptuelle

def get_palet(image, pixel_size):
    list_color = []
    for i in range(image.size[0]//pixel_size):
        for j in range(image.size[1]//pixel_size):
            color_pixel = image.getpixel((i*pixel_size, j*pixel_size))
            if color_pixel not in list_color:
                list_color.append(color_pixel)
    return list_color

def get_nb_pixel(image, size_pixel):
    return image.size[0]//size_pixel , image.size[1]//size_pixel

def normaliser_couleur(r, g, b, pas=60):
    return (
        (r // pas) * pas,
        (g // pas) * pas,
        (b // pas) * pas
    )

palette = get_palet(pixel_art, 16)

for i in range (len(palette)):
    r, g, b, k = palette[i]
    r, g, b = normaliser_couleur(r, g, b)
    palette[i] = r, g, b, k


def distance(c1, c2):
    return math.sqrt(
        (c1[0] - c2[0]) ** 2 +
        (c1[1] - c2[1]) ** 2 +
        (c1[2] - c2[2]) ** 2
    )

def supprimer_doublons_couleurs(palette, seuil=20):
    resultat = []
    for couleur in palette:
        if not any(distance(couleur, c) < seuil for c in resultat):
            resultat.append(couleur)
    return resultat

palette = supprimer_doublons_couleurs(palette)
palette = sorted(palette, key=lambda c: (rgb_to_hsv(c)[0], luminosite(c)))

data = {
    "image" : "discovery_pixel_art.png",
    "pixel_size" : 16,
    "palette" : palette,
    "size_image_pixel" : get_nb_pixel(pixel_art, 16),
    "size_image" : pixel_art.size
}

with open("pixel_art.json", "w") as f:
    json.dump(data, f)

# Charger le JSON
with open("pixel_art.json", "r") as f:
    data = json.load(f)

create_pdf(data)

pixel_art.close()


liste_couleur_disponible = { (55, 0, 40, 255) : "aubergine",
                             ( )

}

