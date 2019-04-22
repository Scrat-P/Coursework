from PIL import Image, ImageDraw, ImageFont
from colour import Color
import numpy as np


INPUT_FILE = "/Users/didred/Documents/БГУИР/ОСиС/Coursework/server/picture.png"
OUTPUT_FILE = "results.png"
SC = 1
GCF = 1.3
make_color = lambda : (randint(50, 255), randint(50, 255), randint(50,255))

def convert():
    rgb_img = Image.open(INPUT_FILE)
    chars = np.asarray(list(' .,:irs?@9B&#'))

    font = ImageFont.load_default()
    letter_width = round(font.getsize("x")[0])
    letter_height = round(font.getsize("x")[1])

    WCF = letter_height / letter_width

    width_by_letter = round(rgb_img.size[0] * SC * WCF)
    height_by_letter = round(rgb_img.size[1] * SC)
    size = (width_by_letter, height_by_letter)

    rgb_img = rgb_img.resize(size)

    img = np.sum(np.asarray(rgb_img), axis = 2)
    rgb_img = np.asarray(rgb_img)

    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)

    lines = ("\n".join( ("".join(r) for r in chars[img.astype(int)]) )).split("\n")

    new_img_width= letter_width * width_by_letter
    new_img_height = letter_height * height_by_letter
    image = Image.new("RGB", (new_img_width, new_img_height), "white")
    draw = ImageDraw.Draw(image)

    y_draw = 0
    for i in range(len(lines)):
        line = lines[i]
        x_draw = 0
        for j in range(len(line)):
            c = line[j]
            x_full, y_full = draw.textsize(c)
            draw.text((x_draw, y_draw), c, (rgb_img[i][j][0], rgb_img[i][j][1], rgb_img[i][j][2]))
            x_draw += x_full
        y_draw += y_full

    image.save(OUTPUT_FILE)

convert()
