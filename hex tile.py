import tkinter as tk
from PIL import Image, ImageTk


class HexTile1(object):
    """A tile that not drawable"""
    height = 0
    width = 0

    numbered = False


class TerrainTile1(HexTile1):
    """A tile that actually has a kind of terrain and drawable"""
    numbered = True
    height = 7
    width = 13

    def __init__(self, number, placement, terrain_kind):
        self.number = number
        self.placement = placement
        self.terrain_kind = terrain_kind
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, bg="#2596be", height=500, width=500)
        self.image_hex_path = "assets\{}_hex_rotated1.png".format(self.terrain_kind)
        self.image_photo = Image.open(self.image_hex_path)
        self.image_photo = ImageTk.PhotoImage(self.image_photo.resize((150, 150), Image.LANCZOS))

    def start(self):
        self.canvas.pack()
        self.draw_tile(self.canvas)
        self.root.mainloop()

    def get_number(self):
        return self.number

    def __repr__(self):
        return f"TerrainTile1:({self.terrain_kind}, {self.placement}, {self.number})"

    def draw_tile(self, canvas):
        canvas.create_image(269, 258, image=self.image_photo)


if __name__ == "__main__":
    tile1 = TerrainTile1(0, (0, 0), "field")
    tile1.start()
