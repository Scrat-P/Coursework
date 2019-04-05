from tkinter import *
from PIL import Image, ImageTk

class Initializer:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Paint")

        self.canvas_width = 1000
        self.canvas_height = 800
        self.background_color = "white"

    def init_canvas(self):
        self.canvas = Canvas(self.main_window)
        self.canvas.pack(expand=YES, fill=BOTH)

        self.img = Image.new("RGB", [self.canvas_width, self.canvas_height], self.background_color)

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, image=self.canvas.img)