from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from threading import Thread
from recipient import Recipient


APP_TITLE = 'Online ASCII-art'
BACKGROUND_COLOR = 'white'
IMG_INITIAL_WIDTH = 1200
IMG_INITIAL_HEIGHT = 800
ABOUT_TITLE = "About app"
FILE_MENU_COMMAND = 'File'
SAVE_AS_MENU_COMMAND = 'Save as...'
EXIT_MENU_COMMAND = 'Exit'
ABOUT_MENU_COMMAND = 'About'
SAVE_AS_MENU_COMMAND = 'Save as...'
ABOUT_MESSAGE = ("Network graphic ASCII-art editor\n"
                 "© 2019 Baranovich & Yurevich")


class ServerApp:
    def __init__(self, main_window):
        self.recipient = Recipient()

        self.main_window = main_window
        self.main_window.title(APP_TITLE)
        self.frame = Frame(self.main_window)

        self.img_width = IMG_INITIAL_WIDTH
        self.img_height = IMG_INITIAL_HEIGHT
        self.background_color = BACKGROUND_COLOR

        self._init_canvas()
        self._init_menubar()
        self._init_setingsbar()

        Thread(target=self.receive_images).start()

    def _init_menubar(self):
        menubar = Menu(self.main_window)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=FILE_MENU_COMMAND, menu=file_menu)
        file_menu.add_command(
            label=SAVE_AS_MENU_COMMAND, command=self.call_save_as_image)
        file_menu.add_command(
            label=EXIT_MENU_COMMAND, command=self.frame.quit)
        menubar.add_command(
            label=ABOUT_MENU_COMMAND, command=self.show_about_app)

        self.main_window.config(menu=menubar)

    def show_about_app(self):
        messagebox.showinfo(ABOUT_TITLE, ABOUT_MESSAGE)

    def call_save_as_image(self):
        file_name = filedialog.asksaveasfilename(defaultextension='.png')

        if file_name is not None:
            self.img.save(file_name)

    def _init_canvas(self):
        self.canvas = Canvas(
            self.main_window, bg=self.background_color)
        self.canvas.pack(expand=1, fill=BOTH)

        self.img = Image.new(
            'RGB', [self.img_width, self.img_height],
            self.background_color
        )

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(
            0, 0, anchor=NW, image=self.canvas.img)

        self.canvas.bind('<Configure>', self.configure)
        
    def configure(self, event):
        self.canvas.delete('all')
        self.img_width = event.width
        self.img_height = event.height

        self.img.resize((self.img_width, self.img_height),
                        Image.LANCZOS)

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(
            0, 0, anchor=NW, image=self.canvas.img)

    def show_ascii(self):
        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(
            0, 0, anchor=NW, image=self.canvas.img)

    def receive_images(self):
        while True:
            self.img = self.recipient.receive_images(
                self.scale, self.contrast)

            self.show_ascii()

    def change_image(self, event=None):
        self.img = self.recipient.change_image(
            self.scale, self.contrast)

        self.show_ascii()

    def _init_setingsbar(self):
        self.setingsbar = Frame(
            self.main_window, borderwidth=0, relief=RAISED)

        self.setingsbar.pack(side=BOTTOM, fill=X)

        self.scale = 0.1
        self.width_scale = Scale(
            self.setingsbar, orient=HORIZONTAL,
            from_=0.1, to=1, sliderlength=15,
            showvalue=0, resolution=0.05,
            command=self.change_scale
        )
        self.width_scale.bind("<ButtonRelease-1>", self.change_image)
        self.width_scale.pack(side=RIGHT)

        self.scale_label = Label(
            self.setingsbar, text='Scale:   0.1 ',)
        self.scale_label.pack(side=RIGHT)

        self.contrast = 0.1
        self.width_contrast = Scale(
            self.setingsbar, orient=HORIZONTAL,
            from_=0.1, to=3, sliderlength=15,
            showvalue=0, resolution=0.1,
            command=self.change_contrast
        )
        self.width_contrast.bind("<ButtonRelease-1>", self.change_image)
        self.width_contrast.pack(side=RIGHT)

        self.contrast_label = Label(
            self.setingsbar, text='Contrast:   0.1 ',)
        self.contrast_label.pack(side=RIGHT)

    def change_scale(self, new_scale):
        self.scale = float(new_scale)
        self.scale_label.configure(text=f'Scale:  {new_scale:>1} ')

    def change_contrast(self, new_contrast):
        self.contrast = float(new_contrast)
        self.contrast_label.configure(
            text=f'Contrast:  {new_contrast:>1} ')


if __name__ == '__main__':
    main_window = Tk()
    main_window.geometry(
        f'{IMG_INITIAL_WIDTH}x{IMG_INITIAL_HEIGHT}')
    main_window.style = ttk.Style()
    main_window.style.theme_use('clam')

    app = ServerApp(main_window)
    main_window.mainloop()