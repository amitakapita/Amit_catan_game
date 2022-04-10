import tkinter as tk
from PIL import Image, ImageTk
import PIL
import random
from tkinter import ttk

x_start, y_start = 250, 95
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
tiles_count = ["lumber" for _ in range(5)] + ["field" for _ in range(5)] + ["wheat" for _ in range(5)] + ["iron" for _
                                                                                                          in
                                                                                                          range(5)] + [
                  "bricks" for _ in range(5)] + ["gold_mine" for _ in range(2)] + ["sea" for _ in range(17)]
numbers = [2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 12, 12]
forbidden_placements = [(1, 5, 6), (0, 2, 6, 7), (1, 3, 7, 8), (2, 4, 8, 9), (3, 9, 10),
                        (0, 6, 11, 12), (0, 1, 5, 7, 12, 13), (1, 2, 6, 8, 13, 14), (2, 3, 7, 9, 14, 15),
                        (3, 4, 8, 10, 15, 16), (4, 9, 16, 17), (5, 12, 18, 19), (5, 6, 11, 13, 19, 20),
                        (6, 7, 12, 14, 20, 21), (7, 8, 13, 15, 21, 22), (8, 9, 14, 16, 22, 23), (9, 10, 15, 17, 23, 24),
                        (10, 16, 24, 25), (11, 19, 26), (11, 12, 18, 20, 26, 27), (12, 13, 19, 21, 27, 28),
                        (13, 14, 20, 22, 28, 29),
                        (14, 15, 21, 23, 29, 30), (15, 16, 22, 24, 30, 31), (16, 17, 23, 25, 31, 32), (17, 24, 32),
                        (18, 19, 27, 33), (19, 20, 26, 28, 33, 34), (20, 21, 27, 29, 34, 35), (21, 22, 28, 30, 35, 36),
                        (22, 23, 29, 31, 36, 37), (23, 24, 30, 32, 37, 38), (24, 25, 31, 38), (26, 27, 34, 39),
                        (27, 28, 33, 35, 39, 40), (28, 29, 34, 36, 40, 41),
                        (29, 30, 35, 37, 41, 42), (30, 31, 36, 38, 42, 43), (31, 32, 37, 43), (33, 34, 40),
                        (34, 35, 39, 41), (35, 36, 40, 42), (36, 37, 41, 43), (37, 38, 42)]
place_numbers_path = r"assets\place_numbers.png"
place_numbers_image = Image.open(place_numbers_path)
numbers_path = r"assets\numbers2.png"
numbers1_image = Image.open(numbers_path)
colors = ["firebrick4", "SteelBlue4", "chartreuse4", "yellow4"]
colors1 = ["red", "blue", "green", "yellow"]


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

    def __init__(self, number, placement, terrain_kind, index):
        self.number = number
        self.placement = placement
        self.terrain_kind = terrain_kind
        self.image_hex_path = "assets\{}_hex_rotated1.png".format(self.terrain_kind[0:])
        self.image_photo = Image.open(self.image_hex_path)
        self.image_photo = ImageTk.PhotoImage(self.image_photo.resize((150, int(150 * (258 / 269))),
                                                                      PIL.Image.Resampling.LANCZOS))  # resampling is the change from the PIL module update
        self.index = index
        if self.terrain_kind != "sea":
            self.place_numbers_image = ImageTk.PhotoImage(
                place_numbers_image.resize((100, 100), PIL.Image.Resampling.LANCZOS))
            self.number_photo = numbers1_image.crop((0 + 40 * (self.number - 1) - 2, 0, 0 + 40 * self.number, 40))
            self.number_photo = self.number_photo.resize((30, 30), PIL.Image.Resampling.LANCZOS)
            self.number_photo = ImageTk.PhotoImage(self.number_photo)

    def get_number(self):
        return self.number

    def __repr__(self):
        return f"TerrainTile1:({self.terrain_kind}, {self.placement}, {self.number}, {self.index})"

    def draw_tile(self, canvas):
        canvas.create_image(self.placement[0], self.placement[1], image=self.image_photo)
        if self.terrain_kind != "sea":
            canvas.create_image(self.placement[0], self.placement[1], image=self.place_numbers_image)
            canvas.create_image(self.placement[0], self.placement[1], image=self.number_photo)

    def change_photo_number(self):
        self.number_photo = numbers1_image.crop((0 + 40 * (self.number - 1) - 2, 0, 0 + 40 * self.number, 40))
        self.number_photo = self.number_photo.resize((30, 30), PIL.Image.Resampling.LANCZOS)
        self.number_photo = ImageTk.PhotoImage(self.number_photo)


class Map(object):
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, bg="#2596be", width=900, highlightbackground="black", highlightthickness=3)
        self.tiles = []

    def start(self):
        self.canvas.pack(side=tk.LEFT)
        self.canvas["height"] = self.root.winfo_screenheight()
        self.generate_map()
        self.draw_map()

    def draw_map(self):
        for index, tile in enumerate(self.tiles):
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
            temp_tile1 = TerrainTile1(temp_number, place, temp_tile, index)
            self.tiles.append(temp_tile1)
        self.check_tile_validation()

    def check_tile_validation(self):
        """
        checks the validation of the map about the tiles, and changes the map if it is necessary
        :return: None
        """
        gold_mine_tiles = []
        for tile in self.tiles:
            if tile.terrain_kind == "gold_mine":
                gold_mine_tiles.append(tile)
        for gold_mine_tile in gold_mine_tiles:
            if gold_mine_tile.number == 6 or gold_mine_tile.number == 8:
                temp_tile = random.choice([tile1 for tile1 in self.tiles if
                                           tile1.number != 6 and tile1.number != 8 and tile1.terrain_kind != "gold_mine" and tile1.terrain_kind != "sea"])
                print(gold_mine_tile, temp_tile)
                self.tiles[gold_mine_tile.index].number, self.tiles[
                    temp_tile.index].number = temp_tile.number, gold_mine_tile.number
                self.tiles[gold_mine_tile.index].change_photo_number()
                self.tiles[temp_tile.index].change_photo_number()
                print(gold_mine_tile, temp_tile)
        if gold_mine_tiles[0].index in forbidden_placements[gold_mine_tiles[1].index]:
            tile_xchange = random.choice(
                self.tiles[:gold_mine_tiles[0].index] + self.tiles[gold_mine_tiles[1].index + 1:] + self.tiles[
                                                                                                    gold_mine_tiles[
                                                                                                        0].index + 1:
                                                                                                    gold_mine_tiles[
                                                                                                        1].index])  # tile_xchange points to the same id in the memory as the selected tile
            while tile_xchange.index in forbidden_placements[gold_mine_tiles[1].index]:
                tile_xchange = random.choice(
                    self.tiles[:gold_mine_tiles[0].index] + self.tiles[gold_mine_tiles[1].index + 1:] + self.tiles[
                                                                                                        gold_mine_tiles[
                                                                                                            0].index + 1:
                                                                                                        gold_mine_tiles[
                                                                                                            1].index])  # tile_xchange points to the same id in the memory as the selected tile
            self.tiles[gold_mine_tiles[0].index].placement, self.tiles[
                tile_xchange.index].placement = tile_xchange.placement, gold_mine_tiles[0].placement
            self.tiles[gold_mine_tiles[0].index].index, self.tiles[tile_xchange.index].index = tile_xchange.index, \
                                                                                               gold_mine_tiles[0].index
            self.tiles[gold_mine_tiles[0].index], self.tiles[tile_xchange.index] = self.tiles[tile_xchange.index], \
                                                                                   self.tiles[gold_mine_tiles[0].index]

    def __repr__(self):
        return [tile.__repr__() for tile in self.tiles]


class StatsScreen(object):
    def __init__(self, root):
        self.root = root
        self.note_book_players = ttk.Notebook(self.root, width=self.root.winfo_screenwidth() - 900, padding="0.05i", style="TNotebook")
        self.list_of_contents = []

    def start(self, list1):
        self.note_book_players.pack(anchor=tk.NE, expand=True, pady=20, padx=20)
        self.note_book_players.enable_traversal()  # can navigate with Ctrl + Shift + Tab, Ctrl + Tab
        for i, name in enumerate(list1):
            self.add_note(name, i)

    def add_note(self, name, i):
        frame = tk.Frame(self.note_book_players, bg="#2596be")
        lbl0 = tk.Label(frame, text=f"color: {colors1[i]}", font="Arial 15", bg="#2596be", fg=colors[i])
        lbl1 = tk.Label(frame, text=f"points: 12", font="Arial 15", bg="#2596be")
        lbl2 = tk.Label(frame, text="number of resources: 7", font="Arial 15", bg="#2596be")
        lbl3 = tk.Label(frame, text="number of development cards: 3", font="Arial 15", bg="#2596be")
        self.list_of_contents.append(frame)
        self.list_of_contents.append(lbl0)
        self.list_of_contents.append(lbl1)
        self.list_of_contents.append(lbl2)
        self.list_of_contents.append(lbl3)
        frame.pack(fill="both", expand=True)
        lbl0.pack(padx=10, pady=10, anchor=tk.NW)
        lbl1.pack(padx=10, pady=5, anchor=tk.NW)
        lbl2.pack(padx=10, pady=5, anchor=tk.NW)
        lbl3.pack(padx=10, pady=5, anchor=tk.NW)
        self.note_book_players.add(frame, text=name)

    def number_of_notes(self):
        return self.note_book_players.index("end") + 1  # the number of the last index + 1 I think

    def names_of_the_tabs(self):
        return self.note_book_players.tabs()

    def change_notes(self, list1):
        for index, content in list1:
            self.list_of_contents[index] = content


if __name__ == "__main__":
    # tile1 = TerrainTile1(0, (0, 0), "field")
    # print(tiles_count)
    # sources = {"lumber": 5, "field": 5, "wheat": 5, "iron": 5, "bricks": 5, "gold_mine": 2, "sea": 17}  # total: 44
    # print(tiles) not to delete
    # tile1.start()

    root = tk.Tk()
    root.configure(bg="#2596be")
    map1 = Map(root=root)
    map1.start()
    style1 = ttk.Style()
    style1.theme_create("notebook_style_catan", settings={
        "TNotebook":
            {"configure":
                 {"background": "DeepSkyBlue4"}},
        "TNotebook.Tab":
            {"configure":
                 {"background": "SkyBlue2",
                  "font": "Arial 15"},
             "map":
                 {"background": [("selected", "SkyBlue3")],  # when selected
                  "expand": [("selected", [0, 5, 0, 0])]}}  # when selected the expanding of the tab
    })
    style1.configure("Catan_game_style.TNotebook", highlightbackground="black", highlightthickness=3)
    style1.theme_use("notebook_style_catan")
    stats_screen1 = StatsScreen(root)
    stats_screen1.start(["meow", "meow"])
    #     lbl1 = tk.Label(root, text="meow", font="Arial 15")
    #     lbl1.pack(side=tk.RIGHT)
    # stats_screen1.add_note("meow")
    # stats_screen1.add_note("meow") not to delete
    button_buy_road = tk.Button(root, text="Buy Road", relief="solid", font="Arial 15", bg="SkyBlue3", activebackground="SkyBlue2")
    button_buy_boat = tk.Button(root, text="Buy Boat", relief="solid", font="Arial 15", bg="SkyBlue3", activebackground="SkyBlue2")
    button_buy_settlement = tk.Button(root, text="Buy Settlement", relief="solid", font="Arial 15", bg="SkyBlue3", activebackground="SkyBlue2")
    button_buy_city = tk.Button(root, text="Buy City", relief="solid", font="Arial 15", bg="SkyBlue3", activebackground="SkyBlue2")
    button_buy_development_card = tk.Button(root, text="Buy Development Card", relief="solid", font="Arial 15", bg="SkyBlue3", activebackground="SkyBlue2")
    button_declare_victory = tk.Button(root, text="Declare Victory", relief="solid", font="Arial 15", bg="SkyBlue3", activebackground="SkyBlue2")
    button_next_turn = tk.Button(root, text="Finished My Turn", relief="solid", font="Arial 15", bg="SkyBlue3", activebackground="SkyBlue2")
    button_buy_road.place(x=root.winfo_screenwidth() - 125, y=root.winfo_screenheight() - 400)
    button_buy_boat.place(x=root.winfo_screenwidth() - 250, y=root.winfo_screenheight() - 400)
    button_buy_settlement.place(x=root.winfo_screenwidth() - 430, y=root.winfo_screenheight() - 400)
    button_buy_city.place(x=root.winfo_screenwidth() - 112, y=root.winfo_screenheight() - 300)
    button_buy_development_card.place(x=root.winfo_screenwidth() - 352, y=root.winfo_screenheight() - 300)
    button_declare_victory.place(x=root.winfo_screenwidth() - 174, y=root.winfo_screenheight() - 200)
    button_next_turn.place(x=root.winfo_screenwidth() - 367, y=root.winfo_screenheight() - 200)
    root.mainloop()
