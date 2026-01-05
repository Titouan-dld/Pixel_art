from PIL import Image

image = Image.open('couleur.xcf')

r,g,b = 0,0,0
for i in range(image.size[0]):
    for j in range(image.size[1]):
        r += image.getpixel(i,j)[0]
        g += image.getpixel(i,j)[1]
        b += image.getpixel(i,j)[2]

r = r//(image.size[0]*image.size[1])
g = g//(image.size[0]*image.size[1])
b = b//(image.size[0]*image.size[1])

print(r,g,b)