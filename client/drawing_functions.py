import math
from PIL import Image, ImageTk, ImageDraw
from main import DARK_COLOR, WHITE_COLOR


def draw_with_pencil_tool(previous_point, current_point, color, img, width):
    draw = ImageDraw.Draw(img)    
    draw.line((previous_point, previous_point, current_point, current_point), color, width, joint='curve')

    return img


def draw_with_ellipse_tool(top_left_point, bottom_right_point, color, img, default_state, width):
    if default_state == 1:
        diameter = max(bottom_right_point[0] - top_left_point[0], bottom_right_point[1] - top_left_point[1])
        bottom_right_point = (top_left_point[0] + diameter, top_left_point[1] + diameter)

    draw = ImageDraw.Draw(img)    
    draw.ellipse((top_left_point, bottom_right_point), outline=color, width=width)

    return img


def draw_with_rectangle_tool(top_left_point, bottom_right_point, color, img, default_state, width):
    if default_state == 1:
        width = max(bottom_right_point[0] - top_left_point[0], bottom_right_point[1] - top_left_point[1])
        bottom_right_point = (top_left_point[0] + width, top_left_point[1] + width)

    draw = ImageDraw.Draw(img)  
    draw.rectangle((top_left_point, bottom_right_point), outline=color, width=width)

    return img


def draw_with_rhomb_tool(top_left_point, bottom_right_point, color, img, default_state, width):
    if default_state == 1:
        width = max(bottom_right_point[0] - top_left_point[0], bottom_right_point[1] - top_left_point[1])
        bottom_right_point = (top_left_point[0] + width, top_left_point[1] + width)

    rhomb_angles = [
        (int((bottom_right_point[0] + top_left_point[0])/2), top_left_point[1]),
        (bottom_right_point[0], int((bottom_right_point[1] + top_left_point[1])/2)),
        (int((bottom_right_point[0] + top_left_point[0])/2), bottom_right_point[1]),
        (top_left_point[0], int((bottom_right_point[1] + top_left_point[1])/2))
    ]

    img = draw_polygon(rhomb_angles, color, width, img)

    return img


def draw_with_star_tool(top_left_point, bottom_right_point, color, img, default_state, width):
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

    img = draw_polygon(star_angles, color, width, img)

    return img


def draw_with_arrow_right_tool(top_left_point, bottom_right_point, color, img, default_state, width):
    if default_state == 1:
        width = max(bottom_right_point[0] - top_left_point[0], bottom_right_point[1] - top_left_point[1])
        bottom_right_point = (top_left_point[0] + width, top_left_point[1] + width)

    a = (bottom_right_point[1] - top_left_point[1])/2.
    b = (bottom_right_point[0] - top_left_point[0])/2.    

    arrow_right_angles = [
        (int(top_left_point[0]), int(a/2 + top_left_point[1])),
        (int(top_left_point[0] + 4*b/3), int(a/2 + top_left_point[1])),
        (int(top_left_point[0] + 4*b/3), int(top_left_point[1])),
        (int(top_left_point[0] + 2*b), int(a + top_left_point[1])),
        (int(top_left_point[0] + 4*b/3), int(2*a + top_left_point[1])),
        (int(top_left_point[0] + 4*b/3), int(3*a/2 + top_left_point[1])),
        (int(top_left_point[0]), int(3*a/2 + top_left_point[1]))
    ]

    img = draw_polygon(arrow_right_angles, color, width, img)

    return img


def erase_rectangle(current_point, color, img):
    draw = ImageDraw.Draw(img)    

    bottom_right_point = (current_point[0] + 5, current_point[1] + 5)
    top_left_point = (current_point[0] - 5, current_point[1] - 5)
    
    draw.rectangle((top_left_point, bottom_right_point), fill=color)

    return img


def draw_with_line_tool(start_point, end_point, color, img, default_state, width):
    if default_state == 1:
        if abs(end_point[0] - start_point[0]) >= abs(end_point[1] - start_point[1]):
            end_point[1] = start_point[1]
        else:
            end_point[0] = start_point[0]

    draw = ImageDraw.Draw(img)    
    draw.line(start_point + end_point, color, width)

    return img


def fill_color(point, color, img):
    ImageDraw.floodfill(img, point, color)

    return img


def draw_scalealealealealing(selected_area, cursor_position, background_color, img):
    selected_img = img.crop(selected_area)

    top_left_point = (selected_area[0], selected_area[1])
    bottom_right_point = (selected_area[2], selected_area[3])
    img = erase_selected_area(top_left_point, bottom_right_point, background_color, img)

    scaled_img_width = abs(cursor_position[0] - selected_area[0])
    scaled_img_heigth = abs(cursor_position[1] - selected_area[1])
    scaled_img = selected_img.resize((scaled_img_width, scaled_img_heigth))

    img.paste(scaled_img, (selected_area[0], selected_area[1]))

    return img


def erase_selected_area(top_left_point, bottom_right_point, background_color, img):
    draw = ImageDraw.Draw(img)
    draw.rectangle((top_left_point, bottom_right_point), fill=WHITE_COLOR)

    return img


def get_pixel_list(selected_area, selected_img):
    pixel_list = []
    selected_area_width = selected_area[2] - selected_area[0]
    for i in range(selected_area[1], selected_area[3]):
        for j in range(selected_area[0], selected_area[2]):
            color = selected_img[(i - selected_area[1]) * selected_area_width + (j - selected_area[0])]
            pixel_list.append(((j, i), color))

    return pixel_list


def draw_rotating(selected_area, cursor_position, background_color, img):
    selected_img = img.crop(selected_area).getdata()

    pixel_list = get_pixel_list(selected_area, selected_img)

    top_left_point = (selected_area[0], selected_area[1])
    bottom_right_point = (selected_area[2] - 1, selected_area[3] - 1)
    img = erase_selected_area(top_left_point, bottom_right_point, background_color, img)

    top_x, top_y = bottom_right_point
    bottom_x, bottom_y = cursor_position

    if bottom_x > top_x:
        alpha = math.atan((top_y-bottom_y) / float(top_x-bottom_x))    
    else:
        alpha = math.pi + math.atan((top_y-bottom_y) / float(top_x-bottom_x+1e-9))   

    center_x, center_y = top_left_point[0], bottom_right_point[1]
    for i in range(0, len(pixel_list) - 1):
        pixel = pixel_list[i]

        x = center_x + int(math.cos(alpha)*(pixel[0][0] - center_x) - math.sin(alpha)*(pixel[0][1] - center_y))
        y = center_y + int(math.sin(alpha)*(pixel[0][0] - center_x) + math.cos(alpha)*(pixel[0][1] - center_y))

        img.putpixel((x, y), pixel[1])

    return img


def draw_flip_horizontal(selected_area, background_color, img):
    selected_img = img.crop(selected_area)
    flipped_img = selected_img.transpose(Image.FLIP_TOP_BOTTOM)

    img.paste(flipped_img, (selected_area[0], selected_area[1]))

    return img


def draw_flip_vertical(selected_area, background_color, img):
    selected_img = img.crop(selected_area)
    flipped_img = selected_img.transpose(Image.FLIP_LEFT_RIGHT)

    img.paste(flipped_img, (selected_area[0], selected_area[1]))

    return img


def draw_moving(selected_area, cursor_position, background_color, img):
    selected_img = img.crop(selected_area)

    top_left_point = (selected_area[0], selected_area[1])
    bottom_right_point = (selected_area[2] - 1, selected_area[3] - 1)
    img = erase_selected_area(top_left_point, bottom_right_point, background_color, img)

    img.paste(selected_img, cursor_position)

    return img


def draw_with_curve_tool(start_point, cursor_position, end_point, color, img, width):
    t = 0
    previous_point = None
    draw = ImageDraw.Draw(img)
    while t < 1:
        x = int(start_point[0] * (1-t)**2 + 2*(1-t)*t*cursor_position[0] + end_point[0] * t**2)
        y = int(start_point[1] * (1-t)**2 + 2*(1-t)*t*cursor_position[1] + end_point[1] * t**2)
        t = t + 0.001

        if previous_point is not None:
            draw.line([previous_point, previous_point, (x, y), (x, y)], color, width, joint='curve')
        previous_point = (x, y)

    return img


def draw_polygon(polygon_angles, color, width, img):
    draw = ImageDraw.Draw(img)

    polygon_angles.append(polygon_angles[0])
    polygon_angles.append(polygon_angles[1])

    draw.line(polygon_angles, color, width, joint='curve')

    return img
