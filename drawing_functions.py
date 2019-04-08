from PIL import Image, ImageTk, ImageDraw


def draw_with_pencil(previous_point, current_point, color, img):
    draw = ImageDraw.Draw(img)    
    draw.line((previous_point, current_point), color)

    pencil_img = ImageTk.PhotoImage(img)
    return pencil_img