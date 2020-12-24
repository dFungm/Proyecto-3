from tkinter import *

class Window:
    def __init__(self):
        self.window = Toplevel()
        self.window.configure(background='black')
        self.window.geometry("200x200")

        width = 100
        height = 100
        self.canvas = Canvas(self.window, width = width, height = height, bg = "#000000")
        self.canvas.pack()
        img = PhotoImage(width = width, height = height)
        img = img.subsample(10)
        self.canvas.create_image((width // 2, height // 2), image = img, state = "normal")

    def paint(self, x, y, color):
        mycolor = '#%02x%02x%02x' % color
        self.canvas.create_rectangle(x, y, x, y, outline = mycolor)
