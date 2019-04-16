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


def draw_with_rectangle_tool(top_left_point, bottom_right_point, color, img, default_state):
    if default_state == 1:
        width = max(bottom_right_point[0] - top_left_point[0], bottom_right_point[1] - top_left_point[1])
        bottom_right_point = (top_left_point[0] + width, top_left_point[1] + width)

    draw = ImageDraw.Draw(img)  
    draw.rectangle((top_left_point, bottom_right_point), outline=color)

    return ImageTk.PhotoImage(img)


def draw_with_rhomb_tool(top_left_point, bottom_right_point, color, img, default_state):
    if default_state == 1:
        width = max(bottom_right_point[0] - top_left_point[0], bottom_right_point[1] - top_left_point[1])
        bottom_right_point = (top_left_point[0] + width, top_left_point[1] + width)

    rhomb_angles = [
        (int((bottom_right_point[0] + top_left_point[0])/2), top_left_point[1]),
        (bottom_right_point[0], int((bottom_right_point[1] + top_left_point[1])/2)),
        (int((bottom_right_point[0] + top_left_point[0])/2), bottom_right_point[1]),
        (top_left_point[0], int((bottom_right_point[1] + top_left_point[1])/2))
    ]

    draw = ImageDraw.Draw(img)
    draw.polygon(rhomb_angles, outline=color)

    return ImageTk.PhotoImage(img)


def draw_with_star_tool(top_left_point, bottom_right_point, color, img, default_state):
    if default_state == 1:
        width = max(bottom_right_point[0] - top_left_point[0], bottom_right_point[1] - top_left_point[1])
        bottom_right_point = (top_left_point[0] + width, top_left_point[1] + width)

    a = (bottom_right_point[1] - top_left_point[1])/2.
    b = (bottom_right_point[0] - top_left_point[0])/2.    

    star_angles = [
        (int(top_left_point[0] + b), int(top_left_point[1])),
        (int(top_left_point[0] + 3*b/4), int(top_left_point[1] + a/2)),
        (int(top_left_point[0]), int(top_left_point[1]) + a/2),
        (int(top_left_point[0] + b/2), int(top_left_point[1] + a)),
        (int(top_left_point[0]), int(top_left_point[1] + 1.5*a)),
        (int(top_left_point[0] + 3*b/4), int(top_left_point[1] + 1.5*a)),
        (int(top_left_point[0] + b), int(top_left_point[1] + 2*a)),
        (int(top_left_point[0] + 1.25*b), int(top_left_point[1] + 1.5*a)),
        (int(top_left_point[0] + 2*b), int(top_left_point[1] + 1.5*a)),
        (int(top_left_point[0] + 1.5*b), int(top_left_point[1] + a)),
        (int(top_left_point[0] + 2*b), int(top_left_point[1] + a/2)),
        (int(top_left_point[0] + 1.25*b), int(top_left_point[1] + a/2))
    ]
    
    draw = ImageDraw.Draw(img)
    draw.polygon(star_angles, outline=color)

    return ImageTk.PhotoImage(img)


def erase_rectangle(current_point, color, img):
    draw = ImageDraw.Draw(img)    

    bottom_right_point = (current_point[0] + 5, current_point[1] + 5)
    top_left_point = (current_point[0] - 5, current_point[1] - 5)
    
    draw.rectangle((top_left_point, bottom_right_point), fill=color)

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