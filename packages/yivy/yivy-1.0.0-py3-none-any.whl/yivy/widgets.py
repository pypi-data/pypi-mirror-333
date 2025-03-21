from .core import Label, Button

class Entry:
    def __init__(self, placeholder="", font=("Arial", 12)):
        self.widget = ttk.Entry(font=font)
        self.widget.insert(0, placeholder)

    def pack(self):
        self.widget.pack()

    def get_text(self):
        return self.widget.get()