from PIL import Image, ImageDraw, ImageFont
from colour import Color
import numpy as np


SCALE = 0.1
CONTRAST = 0.3


class Converter():
    def __init__(self, image):
        self.scale = SCALE
        self.contrast = CONTRAST
        self.rgb_img = image


    def convert(self):
        chars = np.asarray(list(' .,:irs?@9B&#'))

        font = ImageFont.load_default()
        letter_width = round(font.getsize("x")[0])
        letter_height = round(font.getsize("x")[1])

        WCF = letter_height / letter_width

        width_by_letter = round(self.rgb_img.size[0] * self.scale * WCF)
        height_by_letter = round(self.rgb_img.size[1] * self.scale)
        size = (width_by_letter, height_by_letter)

        rgb_img = self.rgb_img.resize(size)

        img = np.sum(np.asarray(rgb_img), axis = 2)
        rgb_img = np.asarray(rgb_img)

        img -= img.min()
        img = (1.0 - img / img.max()) ** self.contrast * (chars.size - 1)

        new_img_width= letter_width * width_by_letter
        new_img_height = letter_height * height_by_letter
        image = Image.new("RGB", (new_img_width, new_img_height), "white")
        draw = ImageDraw.Draw(image)

        if (np.isnan(np.asarray(img)[0][0])):
            image_lines = []
            for i in range(len(img.astype(int))):
                line = []
                for j in range(len(img.astype(int)[i])):
                    line.append(12)
                image_lines.append(line)
            lines = ("\n".join(("".join(r) for r in chars[image_lines]))).split("\n")
        else:
            lines = ("\n".join(("".join(r) for r in chars[img.astype(int)]))).split("\n")

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

        return image
