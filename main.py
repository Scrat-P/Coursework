import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


IMAGES_FOLDER_PATH = 'images'


class App(dict):
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Paint")

        self.canvas_width = 1000
        self.canvas_height = 800
        self.background_color = "white"

        self._init_canvas()
        self._init_menubar()
        self._init_icon_toolbar()
        self._init_color_picker()

    def _init_canvas(self):
        self.canvas = Canvas(self.main_window, bg=self.background_color)
        self.canvas.pack(expand=1, fill=BOTH)

        self.img = Image.new("RGB", [self.canvas_width, self.canvas_height], self.background_color)

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.canvas.img)

    def _init_menubar(self):
        menubar = Menu(self.main_window)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save as...")
        file_menu.add_command(label="Exit")

        menubar.add_command(label="About")

        self.main_window.config(menu=menubar)

    def _create_button_image(self, img, size):
        image_path = os.path.join(IMAGES_FOLDER_PATH, f"{img}.png")
        img_obj = Image.open(image_path).resize(size, Image.ANTIALIAS)
        self[img] = ImageTk.PhotoImage(img_obj)

    def _init_icon_toolbar(self):
        self._create_button_image('dark_img', (20, 20))
        self._create_button_image('red_img', (20, 20))
        self._create_button_image('green_img', (20, 20))
        self._create_button_image('yellow_img', (20, 20))
        self._create_button_image('orange_img', (20, 20))
        self._create_button_image('purple_img', (20, 20))
        self._create_button_image('blue_malibu_img', (20, 20))
        self._create_button_image('blue_light_img', (20, 20))
        self._create_button_image('pink_img', (20, 20))

    def _create_button(self, toolbar, img, button_name, button_event):
        self[button_name] = Button(toolbar, image=img, command=button_event)
        self[button_name].pack(side=LEFT, fill=X)

    def _init_color_picker(self):
        self.color_toolbar = Frame(self.main_window, borderwidth=2, relief='raised')

        self._create_button(self.color_toolbar, self['dark_img'], 'dark_btn', lambda: self.on_change_color(dark, 'dark_btn'))
        self._create_button(self.color_toolbar, self['red_img'], 'red_btn', lambda: self.on_change_color(red, 'red_btn'))
        self._create_button(self.color_toolbar, self['green_img'], 'green_btn', lambda: self.on_change_color(green, 'green_btn'))
        self._create_button(self.color_toolbar, self['yellow_img'], 'yellow_btn', lambda: self.on_change_color(yellow, 'yellow_btn'))
        self._create_button(self.color_toolbar, self['orange_img'], 'orange_btn', lambda: self.on_change_color(orange, 'orange_btn'))
        self._create_button(self.color_toolbar, self['pink_img'], 'pink_btn', lambda: self.on_change_color(pink, 'pink_btn'))
        self._create_button(self.color_toolbar, self['blue_light_img'], 'blueLight_btn', lambda: self.on_change_color(blueLight, 'blueLight_btn'))
        self._create_button(self.color_toolbar, self['blue_malibu_img'], 'blueMalibu_btn', lambda: self.on_change_color(blueMalibu, 'blueMalibu_btn'))
        self._create_button(self.color_toolbar, self['purple_img'], 'purple_btn', lambda: self.on_change_color(purple, 'purple_btn'))

        self.color_toolbar.pack(side=BOTTOM, fill=X)

    def on_change_color():
        pass


if __name__ == "__main__":
    main_window = Tk()
    main_window.geometry("1000x800")
    main_window.style = ttk.Style()
    main_window.style.theme_use('clam')

    app = App(main_window)
    main_window.mainloop()