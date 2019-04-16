from PIL import Image, ImageTk, ImageDraw


def draw_with_pencil_tool(previous_point, current_point, color, img):
    draw = ImageDraw.Draw(img)    
    draw.line((previous_point, current_point), color)

    return ImageTk.PhotoImage(img)


def draw_with_ellipse_tool(top_left_point, bottom_right_point, color, img, default_state):
    if default_state == 1:
        diameter = max(bottom_right_point[0] - top_left_point[0], bottom_right_point[1] - top_left_point[1])
        bottom_right_point = (top_left_point[0] + diameter, top_left_point[1] + diameter)

    draw = ImageDraw.Draw(img)    
    draw.ellipse((top_left_point, bottom_right_point), outline=color)

    return ImageTk.PhotoImage(img)


def draw_with_line_tool(start_point, end_point, color, img, default_state):
    if default_state == 1:
        if abs(end_point[0] - start_point[0]) >= abs(end_point[1] - start_point[1]):
            end_point[1] = start_point[1]
        else:
            end_point[0] = start_point[0]

    draw = ImageDraw.Draw(img)    
    draw.line(start_point + end_point, color)

    return ImageTk.PhotoImage(img)


def fill_color(point, color, img):
    draw = ImageDraw.floodfill(img, point, color)

    return ImageTk.PhotoImage(img)