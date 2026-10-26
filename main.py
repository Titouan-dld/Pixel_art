from PIL import Image
import json
from generation_pdf import create_pdf
import math
import colorsys

cles_rgb_hama = [(255, 255, 255), (255, 253, 230), (255, 220, 0), (255, 130, 0), (220, 20, 60), (255, 150, 180), (110, 40, 140), (0, 80, 180), (100, 180, 240), (0, 140, 60), (120, 200, 80),
    (120, 60, 20), (240, 245, 250), (255, 240, 150), (100, 110, 50), (200, 160, 210), (128, 128, 128),(30, 30, 30), (245, 245, 245), (230, 80, 90), (80, 150, 220), (80, 180, 110), (150, 100, 180),
    (255, 210, 190), (210, 170, 130), (0, 80, 40), (120, 20, 40), (130, 220, 240), (64, 224, 208), (220, 20, 120), (210, 160, 40), (255, 180, 120), (150, 230, 200), (140, 100, 160),
    (90, 100, 110), (255, 250, 200), (255, 210, 230), (200, 230, 255), (200, 240, 210), (230, 210, 240), (180, 140, 200), (50, 130, 200), (50, 255, 50), (255, 20, 147), (180, 120, 80),
    (140, 70, 50), (110, 90, 80), (190, 190, 190), (80, 80, 80), (255, 255, 0), (255, 100, 0), (170, 220, 0), (10, 30, 80), (255, 200, 150), (180, 40, 90), (255, 170, 130), (40, 100, 60),
    (80, 40, 20), (160, 100, 50), (20, 90, 70), (0, 100, 120), (210, 180, 220), (220, 180, 80), (180, 180, 190), (150, 150, 150), (240, 240, 245), (180, 220, 240), (180, 240, 210), (255, 200, 210),
    (255, 240, 180), (240, 220, 200), (210, 210, 210), (170, 150, 140), (190, 140, 130), (200, 100, 70), (130, 160, 130), (100, 130, 170), (170, 150, 200), (90, 40, 70),
    (60, 60, 70), (90, 100, 70), (255, 120, 100), (230, 60, 140), (50, 110, 160), (0, 120, 90), (60, 30, 20), (245, 240, 230),
]



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

def paletteHama(palette):
    global  cles_rgb_hama
    for i in range (len(palette)):
        distance_min = cles_rgb_hama[0]
        for j in range (len(cles_rgb_hama)):
            if distance(palette[i], cles_rgb_hama[j]) < distance(palette[i], distance_min):
                distance_min = cles_rgb_hama[j]
        palette[i] = distance_min
    return palette

palette = supprimer_doublons_couleurs(palette)
palette = sorted(palette, key=lambda c: (rgb_to_hsv(c)[0], luminosite(c)))
palette = paletteHama(palette)


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

