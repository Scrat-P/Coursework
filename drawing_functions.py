from PIL import Image, ImageTk, ImageDraw


def draw_with_pencil(previous_point, current_point, color, img):
    draw = ImageDraw.Draw(img)    
    draw.line((previous_point, current_point), color)

    return ImageTk.PhotoImage(img)


def draw_with_ellipse_tool(top_left_point, bottom_right_point, color, img):
    draw = ImageDraw.Draw(img)    
    draw.ellipse((top_left_point, bottom_right_point), outline=color)

    return ImageTk.PhotoImage(img)