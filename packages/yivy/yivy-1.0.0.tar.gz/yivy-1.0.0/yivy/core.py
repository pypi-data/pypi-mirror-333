import tkinter as tk
from tkinter import ttk

class YivyApp:
    def __init__(self, title="Yivy App", size="400x300"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.pack()

    def run(self):
        self.root.mainloop()

class Label:
    def __init__(self, text="", font=("Arial", 12)):
        self.widget = ttk.Label(text=text, font=font)

    def pack(self):
        self.widget.pack()

class Button:
    def __init__(self, text="", on_click=None, font=("Arial", 12)):
        self.widget = ttk.Button(text=text, command=on_click, font=font)

    def pack(self):
        self.widget.pack()