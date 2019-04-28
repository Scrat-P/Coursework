import os
import copy
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkcolorpicker import askcolor
from PIL import Image, ImageTk
from sender import Sender
import drawing_functions as df
from threading import Thread


ACTIVE_THEME = 'clam'
APP_TITLE = 'Online Paint'
IMAGES_FOLDER_PATH = '/Users/didred/Documents/БГУИР/ОСиС/Coursework/client/images'
BACKGROUND_COLOR = 'white'
IMG_INITIAL_WIDTH = 1200
IMG_INITIAL_HEIGHT = 800

RED_COLOR = (255, 0, 0)
DARK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
YELLOW_COLOR = (255, 204, 0)
ORANGE_COLOR = (255, 102, 0)
WHITE_COLOR = (255, 255, 255)
PINK_COLOR = (255, 186, 210)
BLUE_LIGHT_COLOR = (0, 153, 204)
BLUE_MALIBU_COLOR = (102, 204, 255)
PURPLE_COLOR = (102, 0, 204)

MOUSE_CLICK_ACTION_NAME = '<ButtonPress-1>'
MOUSE_MOTION_ACTION_NAME = '<B1-Motion>'
MOUSE_RELEASE_ACTION_NAME = '<ButtonRelease-1>'
ENTER_ACTION_NAME = '<Enter>'
LEAVE_ACTION_NAME = '<Leave>'
SHIFT_PRESS_ACTION_NAME = '<KeyPress-Shift_L>'
SHIFT_RELEASE_ACTION_NAME = '<KeyRelease-Shift_L>'
ESCAPE_PRESS_ACTION_NAME = '<KeyPress-Escape>'
Q_PRESS_ACTION_NAME = '<q>'
RESIZE_WINDOW_ACTION_NAME = '<Configure>'

WIDTH_LABEL_TEXT = 'Line width'

WATCH_CURSOR = 'watch'
CROSSHAIR_CURSOR = 'crosshair'
ARROW_CURSOR = 'arrow'
DOTBOX_CURSOR = 'dotbox'
CIRCLE_CURSOR = 'circle'
PENCIL_CURSOR = 'pencil'
SPRAYCAN_CURSOR = 'spraycan'

INITIAL_COLOR_BUTTON = 'red_btn'
INITIAL_TOOL_BUTTON = 'pencil_btn'
ACTIVE_COLOR_BUTTON = 'active_color_button'
ACTIVE_TOOL_BUTTON = 'active_tool_button'
COLOR_PALETTE_NAME = 'palette'

FILE_MENU_COMMAND = 'File'
NEW_MENU_COMMAND = 'New'
OPEN_MENU_COMMAND = 'Open...'
SAVE_AS_MENU_COMMAND = 'Save as...'
EXIT_MENU_COMMAND = 'Exit'
EDIT_MENU_COMMAND = 'Edit'
ROLLBACK_TOOL_MENU_COMMAND = 'Rollback tool (esc)'
UNDO_MENU_COMMAND = 'Undo (q)'
ABOUT_MENU_COMMAND = 'About'

ABOUT_TITLE = "About app"
ABOUT_MESSAGE = ("Network graphic ASCII-art editor\n"
                 "© 2019 Baranovich & Yurevich")

OPEN_FILETYPES = (
    ('Supported image files', '*.jpg *.jpeg *.png *.bmp *.ico'),    
    ('All files', '*.*')
) 

MAX_SAVED_IMAGES_COUNT = 30

COLOR_BUTTONS_WIDTH = 20
COLOR_BUTTONS_HEIGHT = 20
COLOR_BUTTONS = (
    ('dark', DARK_COLOR),
    ('white', WHITE_COLOR),
    ('red', RED_COLOR),
    ('green', GREEN_COLOR),
    ('yellow', YELLOW_COLOR),
    ('orange', ORANGE_COLOR),
    ('pink', PINK_COLOR),
    ('blue_light', BLUE_LIGHT_COLOR),
    ('blue_malibu', BLUE_MALIBU_COLOR),
    ('purple', PURPLE_COLOR)
)

MOVE_TOOL = 'move_tool'
ROTATE_TOOL = 'rotate_tool'
SCALE_TOOL = 'scale_tool'
FLIP_VERTICAL_TOOL = 'flip_vertical_tool'
FLIP_HORIZONTAL_TOOL = 'flip_horizontal_tool'
PENCIL_TOOL = 'pencil'
ERASER_TOOL = 'eraser'
LINE_TOOL = 'line'
CURVE_TOOL = 'curve'
ELLIPSE_TOOL = 'ellipse'
RECTANGLE_TOOL = 'rectangle'
RHOMB_TOOL = 'rhomb'
STAR_TOOL = 'star'
ARROW_RIGHT_TOOL = 'arrow_right'
FILL_TOOL = 'fill_tool'

TOOL_BUTTONS_WIDTH = 30
TOOL_BUTTONS_HEIGHT = 30
TOOL_BUTTONS = (
    MOVE_TOOL, ROTATE_TOOL, SCALE_TOOL,
    FLIP_VERTICAL_TOOL, FLIP_HORIZONTAL_TOOL,
    PENCIL_TOOL, ERASER_TOOL, LINE_TOOL,
    CURVE_TOOL, ELLIPSE_TOOL, RECTANGLE_TOOL,
    RHOMB_TOOL, STAR_TOOL, ARROW_RIGHT_TOOL, FILL_TOOL
)

BUTTONS_DESCRIPTION = {
  'move_tool_btn': {
    'title': 'Transition',
    'description': 'Select a region, then click and move the object.'
  },
  'rotate_tool_btn': {
    'title': 'Rotation',
    'description': 'Select a region, then click and rotate the object.'
  },
  'scale_tool_btn': {
    'title': 'Scalling',
    'description': 'Select a region, then click and drag the object.'
  },  
  'flip_vertical_tool_btn': {
    'title': 'Flip vertical',
    'description': 'Select a region, then click.'
  },
  'flip_horizontal_tool_btn': {
    'title': 'Flip horizontal',
    'description': 'Select a region, then click.'
  },
  'pencil_btn': {
    'title': 'Pencil',
    'description': 'Draw pattern.'
  },
  'eraser_btn': {
    'title': 'Eraser',
    'description': 'Erase pattern.'
  },
  'line_btn': {
    'title': 'Line',
    'description': 'Choosing a point, then move the mouse. '
                   'Hold SHIFT to draw vertical or horizontal line.'
  },
  'curve_btn': {
    'title': 'Curve',
    'description': 'Choosing two point, then move the mouse.'
  },
  'ellipse_btn': {
    'title': 'Eclipse',
    'description': 'Choosing a point, then move the mouse. '
                   'Hold SHIFT to draw circle.'
  },
  'rectangle_btn': {
    'title': 'Rectangle',
    'description': 'Choosing a point, then move the mouse. '
                   'Hold SHIFT to draw square.'
  },  
  'rhomb_btn': {
    'title': 'Rhomb shape',
    'description': 'Choosing a point, then move the mouse.'
  },
  'star_btn': {
    'title': 'Star shape',
    'description': 'Choosing a point, then move the mouse.'
  },
  'arrow_right_btn': {
    'title': 'Arrow shape',
    'description': 'Choosing a point, then move the mouse.'
  },
  'fill_tool_btn': {
    'title': 'Fill color',
    'description': 'Choosing a point in region.'
  },
  'dark_btn': {
    'title': 'Dark color',
    'description': ''
  },
  'white_btn': {
    'title': 'White color',
    'description': ''
  },
  'red_btn': {
    'title': 'Red color',
    'description': ''
  },
  'green_btn': {
    'title': 'Green color',
    'description': ''
  },
  'yellow_btn': {
    'title': 'Yellow color',
    'description': ''
  },
  'orange_btn': {
    'title': 'Orange color',
    'description': ''
  },
  'pink_btn': {
    'title': 'Pink color',
    'description': ''
  },
  'blue_light_btn': {
    'title': 'Blue light color',
    'description': ''
  },
  'blue_malibu_btn': {
    'title': 'Blue malibu color',
    'description': ''
  },
  'purple_btn': {
    'title': 'Purple color',
    'description': ''
  },
  'palette_btn': {
    'title': 'Color palette',
    'description': 'Open the palette and choose a color to draw.'
  }
}


class ClientApp(dict):
    def __init__(self, main_window):
        self.main_window = main_window

        self._init_app_settings()
        self._init_icon_toolbar()
        self._init_drawbar()
        self._init_canvas()
        self._init_menubar()
        self._init_color_picker()
        self._init_main_hotkeys()
        self._init_tool_buttons()

    def _init_app_settings(self):
        self.main_window.title(APP_TITLE)
        self.frame = Frame(self.main_window)
        self.image_storage = []

        self.sender = Sender()

        self.img_width = IMG_INITIAL_WIDTH
        self.img_height = IMG_INITIAL_HEIGHT
        self.background_color = BACKGROUND_COLOR
        self.pixel_list = None

    def _init_tool_buttons(self):
        self.active_color = RED_COLOR
        self.active_color_button = self[INITIAL_COLOR_BUTTON]
        self._activate_button(ACTIVE_COLOR_BUTTON, INITIAL_COLOR_BUTTON)

        self.active_tool_button = self[INITIAL_TOOL_BUTTON]

        self.active_tool = self.draw_pencil_tool
        self.active_tool()

    def _init_main_hotkeys(self):
        self.main_window.bind(
            ESCAPE_PRESS_ACTION_NAME, self.rollback_operation)
        self.main_window.bind(Q_PRESS_ACTION_NAME, self.undo_canvas)

        self.main_window.bind(
            SHIFT_PRESS_ACTION_NAME, lambda event: self.on_key_press())
        self.main_window.bind(
            SHIFT_RELEASE_ACTION_NAME, lambda event: self.on_key_release())
        self.default_state = 0

    def run_sending_thread(self):
        Thread(target=self.send_canvas_to_server).start()

    def add_image_to_storage(self, img):
        if len(self.image_storage) >= MAX_SAVED_IMAGES_COUNT:
            self.image_storage = self.image_storage[-(MAX_SAVED_IMAGES_COUNT-1):]
        self.image_storage.append(copy.copy(img))

        self.run_sending_thread()

    def _init_canvas(self):
        self.canvas = Canvas(self.main_window, bg=self.background_color)
        self.canvas.pack(expand=1, fill=BOTH)

        self.img = Image.new(
            'RGB', [self.img_width, self.img_height], 
            self.background_color
        )
        self.add_image_to_storage(self.img)

        self._show_image_on_canvas(self.img)

        self.canvas.bind(RESIZE_WINDOW_ACTION_NAME, self.configure)

    def rollback_operation(self, event=None):
        self._show_image_on_canvas(self.img)

        self.active_tool()

    def undo_canvas(self, event=None):
        if len(self.image_storage) < 2:
            return

        self.img = self.image_storage[-2].resize(
            (self.img_width, self.img_height), Image.LANCZOS)
        self._show_image_on_canvas(self.img)

        self.image_storage = self.image_storage[:-1]

        self.run_sending_thread()
        self.active_tool()

    def configure(self, event):
        self.canvas.delete('all')
        self.img_width = event.width
        self.img_height = event.height

        self.img = self.img.resize(
            (self.img_width, self.img_height), Image.LANCZOS)

        self._show_image_on_canvas(self.img)

    def _init_menubar(self):
        menubar = Menu(self.main_window)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=FILE_MENU_COMMAND, menu=file_menu)
        file_menu.add_command(
            label=NEW_MENU_COMMAND, command=self.call_new_canvas)
        file_menu.add_command(
            label=OPEN_MENU_COMMAND, command=self.call_open_image)
        file_menu.add_command(
            label=SAVE_AS_MENU_COMMAND, command=self.call_save_as_image)
        file_menu.add_separator()
        file_menu.add_command(
            label=EXIT_MENU_COMMAND, command=self.frame.quit)

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=EDIT_MENU_COMMAND, menu=edit_menu)
        edit_menu.add_command(
            label=ROLLBACK_TOOL_MENU_COMMAND, command=self.rollback_operation)
        edit_menu.add_command(
            label=UNDO_MENU_COMMAND, command=self.undo_canvas)

        menubar.add_command(
            label=ABOUT_MENU_COMMAND, command=self.show_about_app)

        self.main_window.config(menu=menubar)

    def show_about_app(self):
        messagebox.showinfo(ABOUT_TITLE, ABOUT_MESSAGE)

    def call_save_as_image(self):
        file_name = filedialog.asksaveasfilename(defaultextension='.png')

        if file_name is not None:
            self.img.save(file_name)

    def call_new_canvas(self):
        self.canvas.delete('all')
        self.img = Image.new(
            'RGB', (self.img_width, self.img_height), 
            self.background_color
        )
        self.add_image_to_storage(self.img)

        self._show_image_on_canvas(self.img)

    def call_open_image(self):
        file_name = filedialog.askopenfilename(filetypes=OPEN_FILETYPES)

        if file_name:
            self.canvas.delete('all')

            self.img = Image.open(file_name).resize(
                (self.img_width, self.img_height), Image.LANCZOS)
            self.add_image_to_storage(self.img)

            self._show_image_on_canvas(self.img)

    def _create_button_image(self, img, size):
        image_path = os.path.join(IMAGES_FOLDER_PATH, f'{img}.png')
        img_obj = Image.open(image_path).resize(size, Image.LANCZOS)
        self[img] = ImageTk.PhotoImage(img_obj)

    def _init_icon_toolbar(self):
        for color_name, _ in COLOR_BUTTONS:
            self._create_button_image(
                f'{color_name}_img', 
                (COLOR_BUTTONS_WIDTH, COLOR_BUTTONS_HEIGHT)
            )

        self._create_button_image(
            f'{COLOR_PALETTE_NAME}_img', 
            (COLOR_BUTTONS_WIDTH, COLOR_BUTTONS_HEIGHT)
        )

        for tool_name in TOOL_BUTTONS:
            self._create_button_image(
                f'{tool_name}_img', 
                (TOOL_BUTTONS_WIDTH, TOOL_BUTTONS_HEIGHT)
            )

    def on_enter_button(self, event, button_name):
        content = BUTTONS_DESCRIPTION[button_name]
        button_description = content['title'] + '\n' + content['description']
        self.description_label.configure(text=button_description)

    def on_leave_button(self, enter):
        self.description_label.configure(text='')

    def _create_button(self, toolbar, img, button_name, button_event):
        self[button_name] = Button(toolbar, image=img, command=button_event)

        self[button_name].bind(
            ENTER_ACTION_NAME, 
            lambda event: self.on_enter_button(event, button_name)
        )
        self[button_name].bind(
            LEAVE_ACTION_NAME, 
            lambda event: self.on_leave_button(event)
        )

        self[button_name].pack(side=LEFT, fill=X)

    def _init_drawbar(self):
        self.drawbar = Frame(self.main_window, borderwidth=0, relief=RAISED)

        for tool_name in TOOL_BUTTONS:
            if tool_name.endswith('tool'):
                tool_event = f'draw_{tool_name}'
            else:
                tool_event = f'draw_{tool_name}_tool'

            self._create_button(
                self.drawbar, self[f'{tool_name}_img'], 
                f'{tool_name}_btn', getattr(self, tool_event)
            )

        self.description_label = Label(self.drawbar, text='', width=40)
        self.description_label.pack(side=TOP, fill=X)

        self.drawbar.pack(side=TOP, fill=X)

    def _init_color_picker(self):
        self.color_toolbar = Frame(self.main_window, 
            borderwidth=0, relief=RAISED)

        for color_name, color_rgb in COLOR_BUTTONS:
            self._create_button(
                self.color_toolbar, self[f'{color_name}_img'], 
                f'{color_name}_btn', 
                (lambda x=color_rgb, y=f'{color_name}_btn': 
                    self.on_change_color(x, y))
            )

        self._create_button(
            self.color_toolbar, self[f'{COLOR_PALETTE_NAME}_img'], 
            f'{COLOR_PALETTE_NAME}_btn', lambda: self.on_palette_click()
        )
        self.color_toolbar.pack(side=BOTTOM, fill=X)

        self.line_width = 1
        self.width_scale = Scale(
            self.color_toolbar, orient=HORIZONTAL, 
            from_=1, to=15, sliderlength=15, 
            showvalue=0, command=self.change_line_width
        )
        self.width_scale.pack(side=RIGHT)

        self.line_width_label = Label(
            self.color_toolbar, text=f'{WIDTH_LABEL_TEXT}:   1 ')
        self.line_width_label.pack(side=RIGHT)

    def on_palette_click(self):
        self._activate_button(
            ACTIVE_COLOR_BUTTON, f'{COLOR_PALETTE_NAME}_btn')

        self.active_color = askcolor(GREEN_COLOR, self.main_window)[0]

    def change_line_width(self, new_width):
        self.line_width = int(new_width)
        self.line_width_label.configure(
            text=f'{WIDTH_LABEL_TEXT}:  {new_width:>2} ')

    def on_change_color(self, color, color_button_name):
        self._activate_button(ACTIVE_COLOR_BUTTON, color_button_name)

        self.active_color = color

    def _activate_button(self, button_attr, new_button_name):
        getattr(self, button_attr).config(relief=RAISED)

        setattr(self, button_attr, self[new_button_name])
        getattr(self, button_attr).config(relief=SUNKEN)

    def _unbind_mouse_actions(self):
        self.canvas.unbind(MOUSE_CLICK_ACTION_NAME)
        self.canvas.unbind(MOUSE_MOTION_ACTION_NAME)
        self.canvas.unbind(MOUSE_RELEASE_ACTION_NAME)

    def _bind_mouse_actions(
            self, release_action, 
            motion_action, click_action=None):
        if click_action is not None:
            self.canvas.bind(MOUSE_CLICK_ACTION_NAME, click_action)
        else:
            self.canvas.bind(MOUSE_CLICK_ACTION_NAME, self.on_button_press)

        self.canvas.bind(MOUSE_MOTION_ACTION_NAME, motion_action)
        self.canvas.bind(MOUSE_RELEASE_ACTION_NAME, release_action)

    def draw_pencil_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{PENCIL_TOOL}_btn')

        self.canvas.config(cursor=PENCIL_CURSOR)
        self._bind_mouse_actions(
            lambda event: self.add_image_to_storage(self.img),
            self.on_button_draw_pencil
        )

        self.active_tool = self.draw_pencil_tool

    def draw_move_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{MOVE_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_move_selected_area,
            self.on_button_selected_area_motion
        )

        self.active_tool = self.draw_move_tool

    def on_button_release_move_selected_area(self, event):
        self._create_selected_area(event)

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_move,
            self.on_button_move_motion
        )

    def _on_button_move(self, event, current_canvas_img):
        cursor_position = (event.x, event.y)
        self.moved_img = df.draw_moving(
            self.selected_area, cursor_position, 
            self.background_color, current_canvas_img
        )
        self._show_image_on_canvas(self.moved_img)

    def on_button_release_move(self, event):
        self._on_button_move(event, self.img)
        self.add_image_to_storage(self.moved_img)

        self.default_state = 0
        self.draw_move_tool()

    def on_button_move_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_move(event, current_canvas_img)

    def draw_rotate_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{ROTATE_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_rotate_selected_area,
            self.on_button_selected_area_motion
        )

        self.active_tool = self.draw_rotate_tool

    def on_button_release_rotate_selected_area(self, event):
        self._create_selected_area(event)

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_rotate,
            self.on_button_rotate_motion
        )

    def _on_button_rotate(self, event, current_canvas_img):
        cursor_position = (event.x, event.y)
        self.rotated_img = df.draw_rotating(
            self.selected_area, cursor_position, 
            self.background_color, current_canvas_img
        )
        self._show_image_on_canvas(self.rotated_img)

    def on_button_release_rotate(self, event):
        self._on_button_rotate(event, self.img)
        self.add_image_to_storage(self.rotated_img)

        self.default_state = 0
        self.draw_rotate_tool()

    def on_button_rotate_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_rotate(event, current_canvas_img)

    def _get_rectangle_angles(self, event):
        return (
            (min(self.x, event.x), min(self.y, event.y)),
            (max(self.x, event.x), max(self.y, event.y))   
        )

    def on_button_selected_area_motion(self, event):
        top_left_point, bottom_right_point = self._get_rectangle_angles(event)

        current_canvas_img = copy.copy(self.img)
        self.selected_img = df.draw_with_rectangle_tool(
            top_left_point, bottom_right_point, 
            DARK_COLOR, current_canvas_img, 0, 1
        )
        self._show_image_on_canvas(self.selected_img)

    def draw_scale_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{SCALE_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_scale_selected_area,
            self.on_button_selected_area_motion
        )

        self.active_tool = self.draw_scale_tool

    def on_button_release_scale_selected_area(self, event):
        self._create_selected_area(event)

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_scale,
            self.on_button_scale_motion
        )

    def _on_button_scale(self, event, current_canvas_img):
        cursor_position = (event.x, event.y)
        self.scaled_img = df.draw_scaling(
            self.selected_area, cursor_position, 
            self.background_color, current_canvas_img
        )
        self._show_image_on_canvas(self.scaled_img)

    def on_button_release_scale(self, event):
        self._on_button_scale(event, self.img)
        self.add_image_to_storage(self.scaled_img)

        self.default_state = 0
        self.draw_scale_tool()

    def on_button_scale_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_scale(event, current_canvas_img)

    def draw_flip_vertical_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{FLIP_VERTICAL_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_flip_vertical_selected_area,
            self.on_button_selected_area_motion
        )

        self.active_tool = self.draw_flip_vertical_tool

    def _create_selected_area(self, event):
        self.selected_area = (
            min(self.x, event.x), min(self.y, event.y),
            max(self.x, event.x), max(self.y, event.y)
        )
        self.default_state = 0

    def on_button_release_flip_vertical_selected_area(self, event):
        self._create_selected_area(event)

        self._unbind_mouse_actions()
        self.canvas.config(cursor=ARROW_CURSOR)
        self.canvas.bind(
            MOUSE_RELEASE_ACTION_NAME, self.on_button_flip_vertical)

    def on_button_flip_vertical(self, event):
        self.flipped_img = df.draw_flip_vertical(
            self.selected_area, self.background_color, self.img)
        self._show_image_on_canvas(self.flipped_img)
        self.add_image_to_storage(self.flipped_img)

        self.default_state = 0
        self.draw_flip_vertical_tool()

    def draw_flip_horizontal_tool(self):
        self._activate_button(
            ACTIVE_TOOL_BUTTON, f'{FLIP_HORIZONTAL_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_flip_horizontal_selected_area,
            self.on_button_selected_area_motion
        )

        self.active_tool = self.draw_flip_horizontal_tool

    def on_button_release_flip_horizontal_selected_area(self, event):
        self._create_selected_area(event)

        self._unbind_mouse_actions()
        self.canvas.config(cursor=ARROW_CURSOR)
        self.canvas.bind(
            MOUSE_RELEASE_ACTION_NAME, self.on_button_flip_horizontal)

    def on_button_flip_horizontal(self, event):
        self.flipped_img = df.draw_flip_horizontal(
            self.selected_area, self.background_color, self.img)
        self._show_image_on_canvas(self.flipped_img)
        self.add_image_to_storage(self.flipped_img)

        self.default_state = 0
        self.draw_flip_horizontal_tool()

    def draw_eraser_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{ERASER_TOOL}_btn')

        self.canvas.config(cursor=DOTBOX_CURSOR)
        self._bind_mouse_actions(
            lambda event: self.add_image_to_storage(self.img),
            self.on_button_eraser
        )

        self.active_tool = self.draw_eraser_tool

    def on_button_eraser(self, event):
        previous_point = (self.x, self.y)
        current_point = (event.x, event.y)

        self.eraser_img = df.erase_line(
            previous_point, current_point, self.background_color, self.img)
        self._show_image_on_canvas(self.eraser_img)

        self.on_button_press(event)

    def _on_button_line(self, event, current_canvas_img):
        start_point = [self.x, self.y]
        end_point = [event.x, event.y]

        self.line_img = df.draw_with_line_tool(
            start_point, end_point, self.active_color, 
            current_canvas_img, self.default_state, self.line_width
        )
        self._show_image_on_canvas(self.line_img)

    def on_button_release_line(self, event):
        self._on_button_line(event, self.img)
        self.add_image_to_storage(self.line_img)
        self.default_state = 0

    def on_button_line_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_line(event, current_canvas_img)

    def draw_line_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{LINE_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_line,
            self.on_button_line_motion
        )

        self.active_tool = self.draw_line_tool

    def on_key_press(self):
        self.default_state = 1

    def on_key_release(self):
        self.default_state = 0

    def _show_image_on_canvas(self, img):
        self.canvas.img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.img) 

    def draw_ellipse_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{ELLIPSE_TOOL}_btn')

        self.canvas.config(cursor=CIRCLE_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_ellipse,
            self.on_button_ellipse_motion
        )

        self.active_tool = self.draw_ellipse_tool

    def draw_rectangle_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{RECTANGLE_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_rectangle,
            self.on_button_rectangle_motion
        )

        self.active_tool = self.draw_rectangle_tool

    def _on_button_rectangle(self, event, current_canvas_img):
        top_left_point, bottom_right_point = self._get_rectangle_angles(event)

        self.rectangle_img = df.draw_with_rectangle_tool(
            top_left_point, bottom_right_point, self.active_color, 
            current_canvas_img, self.default_state, self.line_width
        )
        self._show_image_on_canvas(self.rectangle_img)   

    def on_button_rectangle_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_rectangle(event, current_canvas_img)

    def on_button_release_rectangle(self, event):
        self._on_button_rectangle(event, self.img)
        self.add_image_to_storage(self.rectangle_img)
        self.default_state = 0

    def draw_rhomb_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{RHOMB_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_rhomb,
            self.on_button_rhomb_motion
        )

        self.active_tool = self.draw_rhomb_tool

    def _on_button_rhomb(self, event, current_canvas_img):
        top_left_point, bottom_right_point = self._get_rectangle_angles(event)

        self.rhomb_img = df.draw_with_rhomb_tool(
            top_left_point, bottom_right_point, self.active_color, 
            current_canvas_img, self.default_state, self.line_width
        )
        self._show_image_on_canvas(self.rhomb_img)

    def on_button_rhomb_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_rhomb(event, current_canvas_img)

    def on_button_release_rhomb(self, event):
        self._on_button_rhomb(event, self.img)
        self.add_image_to_storage(self.rhomb_img)
        self.default_state = 0

    def draw_star_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{STAR_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_star,
            self.on_button_star_motion
        )

        self.active_tool = self.draw_star_tool

    def _on_button_star(self, event, current_canvas_img):
        top_left_point, bottom_right_point = self._get_rectangle_angles(event)

        self.star_img = df.draw_with_star_tool(
            top_left_point, bottom_right_point, self.active_color, 
            current_canvas_img, self.default_state, self.line_width
        )
        self._show_image_on_canvas(self.star_img)

    def on_button_star_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_star(event, current_canvas_img)

    def on_button_release_star(self, event):
        self._on_button_star(event, self.img)
        self.add_image_to_storage(self.star_img)
        self.default_state = 0

    def draw_curve_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{CURVE_TOOL}_btn')

        self.curve_points = []

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_curve,
            self.on_button_curve_motion,
            self.add_curve_point
        )

        self.active_tool = self.draw_curve_tool

    def add_curve_point(self, event):
        if len(self.curve_points) >= 2:
            self.curve_points = [self.curve_points[-1]]
        self.curve_points.append((event.x, event.y))

    def _on_button_curve(self, event, current_canvas_img):
        if len(self.curve_points) != 2:
            return

        cursor_position = (event.x, event.y)

        self.curve_img = df.draw_with_curve_tool(
            self.curve_points[0], cursor_position, self.curve_points[1], 
            self.active_color, current_canvas_img, self.line_width
        )
        self._show_image_on_canvas(self.curve_img)

    def on_button_curve_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_curve(event, current_canvas_img)

    def on_button_release_curve(self, event):
        self._on_button_curve(event, self.img)

        if len(self.curve_points) == 2:
            self.draw_curve_tool()
            self.add_image_to_storage(self.curve_img)

    def draw_arrow_right_tool(self):
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{ARROW_RIGHT_TOOL}_btn')

        self.canvas.config(cursor=CROSSHAIR_CURSOR)
        self._bind_mouse_actions(
            self.on_button_release_arrow_right,
            self.on_button_arrow_right_motion
        )

        self.active_tool = self.draw_arrow_right_tool

    def _on_button_arrow_right(self, event, current_canvas_img):
        top_left_point, bottom_right_point = self._get_rectangle_angles(event)

        self.arrow_right_img = df.draw_with_arrow_right_tool(
            top_left_point, bottom_right_point, self.active_color, 
            current_canvas_img, self.default_state, self.line_width
        )
        self._show_image_on_canvas(self.arrow_right_img) 

    def on_button_arrow_right_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_arrow_right(event, current_canvas_img)

    def on_button_release_arrow_right(self, event):
        self._on_button_arrow_right(event, self.img)
        self.add_image_to_storage(self.arrow_right_img)
        self.default_state = 0

    def on_button_fill(self, event):
        self.busy()

        self.filled_img = df.fill_color((event.x, event.y), 
            self.active_color, self.img)
        self._show_image_on_canvas(self.filled_img)
        self.add_image_to_storage(self.filled_img)

        self.notbusy(SPRAYCAN_CURSOR)

    def draw_fill_tool(self):
        self._unbind_mouse_actions()
        self._activate_button(ACTIVE_TOOL_BUTTON, f'{FILL_TOOL}_btn')

        self.canvas.config(cursor=SPRAYCAN_CURSOR)
        self.canvas.bind(MOUSE_CLICK_ACTION_NAME, self.on_button_fill)

        self.active_tool = self.draw_fill_tool

    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y

    def _on_button_ellipse(self, event, current_canvas_img):
        top_left_point, bottom_right_point = self._get_rectangle_angles(event)

        self.ellipse_img = df.draw_with_ellipse_tool(
            top_left_point, bottom_right_point, self.active_color, 
            current_canvas_img, self.default_state, self.line_width
        )
        self._show_image_on_canvas(self.ellipse_img)

    def on_button_ellipse_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_ellipse(event, current_canvas_img)

    def on_button_release_ellipse(self, event):
        self._on_button_ellipse(event, self.img)
        self.add_image_to_storage(self.ellipse_img)
        self.default_state = 0

    def on_button_draw_pencil(self, event):
        previous_point = (self.x, self.y)
        current_point = (event.x, event.y)

        self.pencil_img = df.draw_with_pencil_tool(
            previous_point, current_point, self.active_color, 
            self.img, self.line_width
        )
        self._show_image_on_canvas(self.pencil_img)

        self.on_button_press(event)

    def busy(self):
        self.canvas.config(cursor=WATCH_CURSOR)
        self.main_window.update()

    def notbusy(self, cursor = ''):
        self.canvas.config(cursor=cursor)

    def send_canvas_to_server(self):
        img = copy.copy(self.img)
        self.sender.send_image(img, self.img_width, self.img_height)


if __name__ == '__main__':
    main_window = Tk()
    main_window.geometry(f'{IMG_INITIAL_WIDTH}x{IMG_INITIAL_HEIGHT}')
    main_window.style = ttk.Style()
    main_window.style.theme_use(ACTIVE_THEME)

    app = ClientApp(main_window)
    main_window.mainloop()