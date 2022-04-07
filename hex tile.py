import tkinter as tk
from PIL import Image, ImageTk
import PIL
import random

x_start, y_start = 250, 90
placements = [(x_start, y_start),
              (x_start + 100, y_start),
              (x_start + 200, y_start),
              (x_start + 300, y_start),
              (x_start + 400, y_start),
              (x_start - 51, y_start + 86),
              (x_start + 49, y_start + 86),
              (x_start + 149, y_start + 86),
              (x_start + 249, y_start + 86),
              (x_start + 349, y_start + 86),
              (x_start + 449, y_start + 86),
              (x_start - 102, y_start + 172),
              (x_start - 2, y_start + 172),
              (x_start + 98, y_start + 172),
              (x_start + 198, y_start + 172),
              (x_start + 298, y_start + 172),
              (x_start + 398, y_start + 172),
              (x_start + 498, y_start + 172),
              (x_start + -153, y_start + 258),
              (x_start - 53, y_start + 258),
              (x_start + 47, y_start + 258),
              (x_start + 147, y_start + 258),
              (x_start + 247, y_start + 258),
              (x_start + 347, y_start + 258),
              (x_start + 447, y_start + 258),
              (x_start + 547, y_start + 258),
              (x_start + -104, y_start + 344),
              (x_start - 4, y_start + 344),
              (x_start + 96, y_start + 344),
              (x_start + 196, y_start + 344),
              (x_start + 296, y_start + 344),
              (x_start + 396, y_start + 344),
              (x_start + 496, y_start + 344),
              (x_start + -55, y_start + 430),
              (x_start + 45, y_start + 430),
              (x_start + 145, y_start + 430),
              (x_start + 245, y_start + 430),
              (x_start + 345, y_start + 430),
              (x_start + 445, y_start + 430),
              (x_start + -6, y_start + 516),
              (x_start + 94, y_start + 516),
              (x_start + 194, y_start + 516),
              (x_start + 294, y_start + 516),
              (x_start + 394, y_start + 516)]
tiles_count = ["lumber" for _ in range(5)] + ["field" for _ in range(5)] + ["wheat" for _ in range(5)] + ["iron" for _ in range(5)] + ["bricks" for _ in range(5)] + ["gold_mine" for _ in range(2)] + ["sea" for _ in range(17)]
numbers = [2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 12, 12]

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
        self.image_hex_path = "assets\{}_hex_rotated1.png".format(self.terrain_kind[0:])
        self.image_photo = Image.open(self.image_hex_path)
        self.image_photo = ImageTk.PhotoImage(self.image_photo.resize((150, int(150 * (258/269))), PIL.Image.Resampling.LANCZOS))  # resampling is the change from the PIL module update

    def get_number(self):
        return self.number

    def __repr__(self):
        return f"TerrainTile1:({self.terrain_kind}, {self.placement}, {self.number})"

    def draw_tile(self, canvas):
        canvas.create_image(self.placement[0], self.placement[1], image=self.image_photo)


class Map(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, bg="#2596be", height=750, width=1000)
        self.tiles = []

    def start(self):
        self.canvas.pack(anchor=tk.W)
        self.generate_map()
        self.draw_map()
        self.root.mainloop()

    def draw_map(self):
        for tile in self.tiles:
            tile.draw_tile(self.canvas)

    def generate_map(self):
        tiles_count_copy = tiles_count[:]
        numbers_copy = numbers[:]
        print(len(tiles_count_copy), len(numbers_copy), len(tiles_count), len(numbers))
        for index, place in enumerate(placements):
            temp_tile = random.choice(tiles_count_copy)
            tiles_count_copy.remove(temp_tile)
            if temp_tile == "sea":
                temp_number = None
            else:
                temp_number = random.choice(numbers_copy)
                numbers_copy.remove(temp_number)
            print(index, tiles_count_copy, numbers_copy)
            temp_tile1 = TerrainTile1(temp_number, place, temp_tile)
            self.tiles.append(temp_tile1)

    def __repr__(self):
        return [tile.__repr__() for tile in self.tiles]

if __name__ == "__main__":
    # tile1 = TerrainTile1(0, (0, 0), "field")
    # print(tiles_count)
    # sources = {"lumber": 5, "field": 5, "wheat": 5, "iron": 5, "bricks": 5, "gold_mine": 2, "sea": 17}  # total: 44
    # print(tiles) not to delete
    # tile1.start()

    map1 = Map()
    map1.start()
