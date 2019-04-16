import os
import copy
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import drawing_functions as df


APP_TITLE = 'Online Paint'
IMAGES_FOLDER_PATH = 'images'
BACKGROUND_COLOR = 'white'
IMG_INITIAL_WIDTH = 1000
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

COLOR_BUTTONS_WIDTH = 20
COLOR_BUTTONS_HEIGHT = 20
COLOR_BUTTONS = (
    ('dark', DARK_COLOR),
    ('red', RED_COLOR),
    ('green', GREEN_COLOR),
    ('yellow', YELLOW_COLOR),
    ('orange', ORANGE_COLOR),
    ('pink', PINK_COLOR),
    ('blue_light', BLUE_LIGHT_COLOR),
    ('blue_malibu', BLUE_MALIBU_COLOR),
    ('purple', PURPLE_COLOR)
)

TOOL_BUTTONS_WIDTH = 30
TOOL_BUTTONS_HEIGHT = 30
TOOL_BUTTONS = (
    'move_tool',
    'rotate_tool',
    'scale_tool',
    'flip_vertical_tool',
    'flip_horizontal_tool',
    'pencil',
    'eraser',
    'line',
    'curve',
    'ellipse',
    'rectangle',
    'rhomb',
    'star',
    'arrow_right',
    'fill_tool'
)


class App(dict):
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title(APP_TITLE)
        self.frame = Frame(self.main_window)

        self.img_width = IMG_INITIAL_WIDTH
        self.img_height = IMG_INITIAL_HEIGHT
        self.background_color = BACKGROUND_COLOR

        self._init_icon_toolbar()
        self._init_drawbar()
        self._init_canvas()
        self._init_menubar()
        self._init_color_picker()
        
        self.active_color = RED_COLOR
        self.active_color_button = self['red_btn']

        self.active_tool_button = self['line_btn']
        self.default_state = 0

        self.draw_line_tool()

    def _init_canvas(self):
        self.canvas = Canvas(self.main_window, bg=self.background_color)
        self.canvas.pack(expand=1, fill=BOTH)

        self.img = Image.new("RGB", [self.img_width, self.img_height], self.background_color)

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.img)

        self.canvas.bind("<Configure>", self.configure)

    def configure(self, event):
        self.canvas.delete("all")
        self.img_width = event.width
        self.img_height = event.height

        self.img = self.img.resize((self.img_width, self.img_height))

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.img)

    def _init_menubar(self):
        menubar = Menu(self.main_window)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.call_new_canvas)
        file_menu.add_command(label="Open", command=self.call_open_image)
        file_menu.add_command(label="Save as...", command=self.call_save_as_image)
        file_menu.add_command(label="Exit", command=self.frame.quit)

        menubar.add_command(label="About")

        self.main_window.config(menu=menubar)

    def call_save_as_image(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".png")

        if file_name is not None:
            self.img.save(file_name)

    def call_new_canvas(self):
        self.canvas.delete("all")
        self.img = Image.new("RGB", (self.img_width, self.img_height), self.background_color)

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.img)

    def call_open_image(self):
        file_name = filedialog.askopenfilename(
            filetypes=(
                ("Supported image files", "*.jpg *.jpeg *.png *.bmp *.ico"),
                ("All files", "*.*") 
            )
        )

        if file_name is not None:
            self.canvas.delete("all")

            self.img = Image.open(file_name).resize((self.img_width, self.img_height))

            self.canvas.img = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.img)

    def _create_button_image(self, img, size):
        image_path = os.path.join(IMAGES_FOLDER_PATH, f"{img}.png")
        img_obj = Image.open(image_path).resize(size, Image.ANTIALIAS)
        self[img] = ImageTk.PhotoImage(img_obj)

    def _init_icon_toolbar(self):
        for color_name, _ in COLOR_BUTTONS:
            self._create_button_image(f'{color_name}_img', (COLOR_BUTTONS_WIDTH, COLOR_BUTTONS_HEIGHT))

        for tool_name in TOOL_BUTTONS:
            self._create_button_image(f'{tool_name}_img', (TOOL_BUTTONS_WIDTH, TOOL_BUTTONS_HEIGHT))

    def _create_button(self, toolbar, img, button_name, button_event):
        self[button_name] = Button(toolbar, image=img, command=button_event)
        self[button_name].pack(side=LEFT, fill=X)

    def _init_drawbar(self):
        self.drawbar = Frame(self.main_window, borderwidth=0, relief='raised')

        for tool_name in TOOL_BUTTONS:
            if tool_name.endswith('tool'):
                tool_event = f'draw_{tool_name}'
            else:
                tool_event = f'draw_{tool_name}_tool'

            self._create_button(self.drawbar, self[f'{tool_name}_img'], f'{tool_name}_btn', getattr(self, tool_event))

        self.description_btn = Label(self.drawbar, text="", width=40)
        self.description_btn.pack(side="top", fill="x")

        self.drawbar.pack(side=TOP, fill=X)

    def _init_color_picker(self):
        self.color_toolbar = Frame(self.main_window, borderwidth=0, relief='raised')

        for color_name, color_rgb in COLOR_BUTTONS:
            self._create_button(self.color_toolbar, self[f'{color_name}_img'], f'{color_name}_btn', (lambda x=color_rgb, y=f'{color_name}_btn': self.on_change_color(x, y)))

        self.color_toolbar.pack(side=BOTTOM, fill=X)

    def on_change_color(self, color, color_button_name):
        self._activate_button('active_color_button', color_button_name)

        self.active_color = color

    def _activate_button(self, button_attr, new_button_name):
        getattr(self, button_attr).config(relief=RAISED)

        setattr(self, button_attr, self[new_button_name])
        getattr(self, button_attr).config(relief=SUNKEN)

    def _unbind_buttons(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def draw_pencil_tool(self):
        self._activate_button('active_tool_button', 'pencil_btn')

        self.canvas.config(cursor="pencil")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_draw_pencil)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_draw_pencil)

    def draw_move_tool(self):
        pass

    def draw_rotate_tool(self):
        pass

    def draw_scale_tool(self):
        pass

    def draw_flip_vertical_tool(self):
        pass

    def draw_flip_horizontal_tool(self):
        pass

    def draw_eraser_tool(self):
        self._activate_button('active_tool_button', 'rectangle_btn')

        self.canvas.config(cursor="dotbox")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_eraser)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_eraser) 

    def on_button_eraser(self, event):
        current_point = (event.x, event.y)

        self.eraser_img = df.erase_rectangle(current_point, self.background_color, self.img)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.eraser_img)

        self.x = event.x
        self.y = event.y

    def _on_button_line(self, event, current_canvas_img):
        start_point = [self.x, self.y]
        end_point = [event.x, event.y]

        self.line_img = df.draw_with_line_tool(start_point, end_point, self.active_color, current_canvas_img, self.default_state)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.line_img)

    def on_button_release_line(self, event):
        self._on_button_line(event, self.img)
        self.default_state = 0

    def on_button_line_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_line(event, current_canvas_img)

    def draw_line_tool(self):
        self._activate_button('active_tool_button', 'line_btn')

        self.canvas.config(cursor="crosshair")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_line_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_line)

        self.main_window.bind("<KeyPress-Shift_L>", lambda event: self.on_key_press())
        self.main_window.bind("<KeyRelease-Shift_L>", lambda event: self.on_key_release())

    def draw_curve_tool(self):
        pass

    def on_key_press(self):
        self.default_state = 1

    def on_key_release(self):
        self.default_state = 0

    def draw_ellipse_tool(self):
        self._activate_button('active_tool_button', 'ellipse_btn')

        self.canvas.config(cursor="circle")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_ellipse_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_ellipse) 

        self.main_window.bind("<KeyPress-Shift_L>", lambda event: self.on_key_press())
        self.main_window.bind("<KeyRelease-Shift_L>", lambda event: self.on_key_release())

    def draw_rectangle_tool(self):
        self._activate_button('active_tool_button', 'rectangle_btn')

        self.canvas.config(cursor="crosshair")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_rectangle_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_rectangle) 

        self.main_window.bind("<KeyPress-Shift_L>", lambda event: self.on_key_press())
        self.main_window.bind("<KeyRelease-Shift_L>", lambda event: self.on_key_release())

    def _on_button_rectangle(self, event, current_canvas_img):
        top_left_point = (min(self.x, event.x), min(self.y, event.y))
        bottom_right_point = (max(self.x, event.x), max(self.y, event.y))

        self.rectangle_img = df.draw_with_rectangle_tool(top_left_point, bottom_right_point, self.active_color, current_canvas_img, self.default_state)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.rectangle_img)        

    def on_button_rectangle_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_rectangle(event, current_canvas_img)

    def on_button_release_rectangle(self, event):
        self._on_button_rectangle(event, self.img)
        self.default_state = 0

    def draw_rhomb_tool(self):
        self._activate_button('active_tool_button', 'rhomb_btn')

        self.canvas.config(cursor="crosshair")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_rhomb_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_rhomb) 

        self.main_window.bind("<KeyPress-Shift_L>", lambda event: self.on_key_press())
        self.main_window.bind("<KeyRelease-Shift_L>", lambda event: self.on_key_release())

    def _on_button_rhomb(self, event, current_canvas_img):
        top_left_point = (min(self.x, event.x), min(self.y, event.y))
        bottom_right_point = (max(self.x, event.x), max(self.y, event.y))

        self.rhomb_img = df.draw_with_rhomb_tool(top_left_point, bottom_right_point, self.active_color, current_canvas_img, self.default_state)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.rhomb_img)

    def on_button_rhomb_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_rhomb(event, current_canvas_img)

    def on_button_release_rhomb(self, event):
        self._on_button_rhomb(event, self.img)
        self.default_state = 0

    def draw_star_tool(self):
        self._activate_button('active_tool_button', 'star_btn')

        self.canvas.config(cursor="crosshair")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_star_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release_star) 

        self.main_window.bind("<KeyPress-Shift_L>", lambda event: self.on_key_press())
        self.main_window.bind("<KeyRelease-Shift_L>", lambda event: self.on_key_release())

    def _on_button_star(self, event, current_canvas_img):
        top_left_point = (min(self.x, event.x), min(self.y, event.y))
        bottom_right_point = (max(self.x, event.x), max(self.y, event.y))

        self.star_img = df.draw_with_star_tool(top_left_point, bottom_right_point, self.active_color, current_canvas_img, self.default_state)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.star_img)        

    def on_button_star_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_star(event, current_canvas_img)

    def on_button_release_star(self, event):
        self._on_button_star(event, self.img)
        self.default_state = 0

    def draw_arrow_right_tool(self):
        pass

    def on_button_fill(self, event):
        self.busy()

        self.filled_img = df.fill_color((event.x, event.y), self.active_color, self.img)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.filled_img)

        self.notbusy("spraycan")

    def draw_fill_tool(self):
        self._unbind_buttons()
        self._activate_button('active_tool_button', 'fill_tool_btn')

        self.canvas.config(cursor="spraycan")
        self.canvas.bind("<Button-1>", self.on_button_fill)

    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y

    def _on_button_ellipse(self, event, current_canvas_img):
        top_left_point = (min(self.x, event.x), min(self.y, event.y))
        bottom_right_point = (max(self.x, event.x), max(self.y, event.y))

        self.ellipse_img = df.draw_with_ellipse_tool(top_left_point, bottom_right_point, self.active_color, current_canvas_img, self.default_state)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.ellipse_img)        

    def on_button_ellipse_motion(self, event):
        current_canvas_img = copy.copy(self.img)
        self._on_button_ellipse(event, current_canvas_img)

    def on_button_release_ellipse(self, event):
        self._on_button_ellipse(event, self.img)
        self.default_state = 0

    def on_button_draw_pencil(self, event):
        previous_point = (self.x, self.y)
        current_point = (event.x, event.y)

        self.pencil_img = df.draw_with_pencil_tool(previous_point, current_point, self.active_color, self.img)
        self.canvas.create_image(self.img_width / 2, self.img_height / 2, image=self.pencil_img)

        self.x = event.x
        self.y = event.y

    def busy(self):
        self.canvas.config(cursor="watch")
        self.main_window.update()

    def notbusy(self, cursor = ""):
        self.canvas.config(cursor=cursor)


if __name__ == "__main__":
    main_window = Tk()
    main_window.geometry(f'{IMG_INITIAL_WIDTH}x{IMG_INITIAL_HEIGHT}')
    main_window.style = ttk.Style()
    main_window.style.theme_use('clam')

    app = App(main_window)
    main_window.mainloop()