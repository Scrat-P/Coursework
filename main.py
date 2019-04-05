from tkinter import *
from tkinter import ttk
from init import Initializer


class App:
    def __init__(self, main_window):
        initializer = Initializer(main_window)
        initializer.init_canvas()
        initializer.init_menubar()


if __name__ == "__main__":
    main_window = Tk()
    main_window.geometry("1000x800")
    main_window.style = ttk.Style()
    main_window.style.theme_use('clam')

    app = App(main_window)
    main_window.mainloop()