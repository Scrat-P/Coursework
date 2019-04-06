from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


class App:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Paint")

        self.canvas_width = 1000
        self.canvas_height = 800
        self.background_color = "white"

        self._init_canvas()
        self._init_menubar()

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

    def _init_color_picker(self):
        pass


if __name__ == "__main__":
    main_window = Tk()
    main_window.geometry("1000x800")
    main_window.style = ttk.Style()
    main_window.style.theme_use('clam')

    app = App(main_window)
    main_window.mainloop()