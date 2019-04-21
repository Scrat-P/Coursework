from PIL import Image, ImageDraw, ImageFont
from colour import Color
import numpy as np


INPUT_FILE = "picture.png"
OUTPUT_FILE = "results.png"
SC = 0.1
GCF = 1.3 

def convert():
    img = Image.open(INPUT_FILE)
    chars = np.asarray(list(' .,:irs?@9B&#'))

    font = ImageFont.load_default()
    letter_width = round(font.getsize("x")[0])
    letter_height = round(font.getsize("x")[1])

    WCF = letter_height / letter_width

    width_by_letter = round(img.size[0] * SC * WCF)
    height_by_letter = round(img.size[1] * SC)
    size = (width_by_letter, height_by_letter)

    img = img.resize(size)

    img = np.sum(np.asarray(img), axis = 2)

    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)

    lines = ("\n".join( ("".join(r) for r in chars[img.astype(int)]) )).split("\n")

    nbins = len(lines)
    color_range = list(Color("black").range_to(Color("black"), nbins))

    new_img_width= letter_width * width_by_letter
    new_img_height = letter_height * height_by_letter
    new_img = Image.new("RGBA", (new_img_width, new_img_height), "white")
    draw = ImageDraw.Draw(new_img)

    left_padding = 0
    color = color_range[0]
    y = 0
    for line in lines:
        draw.text((left_padding, y), line, color.hex, font=font)
        y += letter_height

    new_img.save(OUTPUT_FILE)


convert()
