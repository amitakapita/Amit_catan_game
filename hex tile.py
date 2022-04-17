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
forbidden_placements = [(None, None, None, 1, 5, 6), (None, None, 0, 2, 6, 7), (None, None, 1, 3, 7, 8), (None, None, 2, 4, 8, 9), (None, None, 3, None, 9, 10),
                        (None, 0, None, 6, 11, 12), (0, 1, 5, 7, 12, 13), (1, 2, 6, 8, 13, 14), (2, 3, 7, 9, 14, 15),
                        (3, 4, 8, 10, 15, 16), (4, None, 9, None, 16, 17), (None, 5, None, 12, 18, 19), (5, 6, 11, 13, 19, 20),
                        (6, 7, 12, 14, 20, 21), (7, 8, 13, 15, 21, 22), (8, 9, 14, 16, 22, 23), (9, 10, 15, 17, 23, 24),
                        (10, None, 16, None, 24, 25), (None, 11, None, 19, None, 26), (11, 12, 18, 20, 26, 27), (12, 13, 19, 21, 27, 28),
                        (13, 14, 20, 22, 28, 29),
                        (14, 15, 21, 23, 29, 30), (15, 16, 22, 24, 30, 31), (16, 17, 23, 25, 31, 32), (17, None, 24, None, 32, None),
                        (18, 19, None, 27, None, 33), (19, 20, 26, 28, 33, 34), (20, 21, 27, 29, 34, 35), (21, 22, 28, 30, 35, 36),
                        (22, 23, 29, 31, 36, 37), (23, 24, 30, 32, 37, 38), (24, 25, None, 31, None, 38), (26, 27, None, 34, None, 39),
                        (27, 28, 33, 35, 39, 40), (28, 29, 34, 36, 40, 41),
                        (29, 30, 35, 37, 41, 42), (30, 31, 36, 38, 42, 43), (31, 32, 37, None, 43, None), (33, 34, None, 40, None, None),
                        (34, 35, 39, 41), (35, 36, 40, 42), (36, 37, 41, 43), (37, 38, 42, None, None, None)]
place_numbers_path = r"assets\place_numbers.png"
place_numbers_image = Image.open(place_numbers_path)
numbers_path = r"assets\numbers2.png"
numbers1_image = Image.open(numbers_path)
colors = ["firebrick4", "SteelBlue4", "chartreuse4", "yellow4"]
colors1 = ["red", "blue", "green", "yellow"]
placements_middle_hexes_vertex_hexes = [([(placement[0] - 27, placement[1] - 44),
                                        (placement[0] + 27, placement[1] - 44),
                                        (placement[0] - 54, placement[1]),
                                        (placement[0] + 54, placement[1]),
                                        (placement[0] - 27, placement[1] + 46),
                                        (placement[0] + 27, placement[1] + 46)],
                                         [(placement[0] + 1, placement[1] - 58),
                                          (placement[0] + 52, placement[1] - 29),
                                          (placement[0] + 52, placement[1] + 29), (placement[0] + 1, placement[1] + 58),
                                          (placement[0] - 52, placement[1] + 29),
                                          (placement[0] - 52, placement[1] - 29)]) for placement in
                                        placements]  # [(places_middle, places_vertex)]
placements_parts_builds_in_game = [[(220, 53), (280, 53), (320, 53), (380, 53), (420, 53), (480, 53), (520, 53), (580, 53), (620, 53), (680, 53),
                                   (199, 95), (301, 95), (401, 95), (501, 95), (601, 95), (701, 95),
                                   (170, 137), (220, 137), (280, 137), (320, 137), (380, 137), (420, 137), (480, 137), (520, 137), (580, 137), (620, 137), (680, 137), (720, 137),
                                   (148, 181), (250, 181), (350, 181), (450, 181), (550, 181), (650, 181), (750, 181),
                                   (118, 225), (178, 225), (218, 225), (278, 225), (318, 225), (378, 225), (418, 225), (478, 225), (518, 225), (578, 225), (618, 225), (678, 225), (718, 225), (768, 225),
                                   (97, 267), (197, 267), (297, 267), (397, 267), (497, 267), (597, 267), (697, 267), (797, 267),
                                   (69, 309), (129, 309), (169, 309), (229, 309), (269, 309), (329, 309), (369, 309), (420, 309), (480, 309), (520, 309), (580, 309), (620, 309), (680, 309), (720, 309), (780, 309), (820, 309),
                                   (46, 353), (146, 353), (246, 353), (346, 353), (446, 353), (546, 353), (646, 353), (746, 353), (846, 353),
                                   (69, 395), (129, 395), (169, 395), (229, 395), (269, 395), (329, 395), (369, 395), (420, 395), (480, 395), (520, 395), (580, 395), (620, 395), (680, 395), (720, 395), (780, 395), (820, 395),
                                   (97, 439), (197, 439), (297, 439), (397, 439), (497, 439), (597, 439), (697, 439), (797, 439),
                                   (118, 481), (178, 481), (218, 481), (278, 481), (318, 481), (378, 481), (418, 481), (478, 481), (518, 481), (578, 481), (618, 481), (678, 481), (718, 481), (768, 481),
                                   (148, 525), (250, 525), (350, 525), (450, 525), (550, 525), (650, 525), (750, 525),
                                   (170, 567), (220, 567), (280, 567), (320, 567), (380, 567), (420, 567), (480, 567), (520, 567), (580, 567), (620, 567), (680, 567), (720, 567),
                                   (199, 611), (301, 611), (401, 611), (501, 611), (601, 611), (701, 611),
                                   (220, 653), (280, 653), (320, 653), (380, 653), (420, 653), (480, 653), (520, 653), (580, 653), (620, 653), (680, 653)],
                                   [(250, 37), (350, 37), (450, 37), (550, 37), (650, 37),
                                    (200, 66), (300, 66), (400, 66), (500, 66), (600, 66), (700, 66),
                                    (200, 124), (300, 124), (400, 124), (500, 124), (600, 124), (700, 124),
                                    (150, 153), (250, 153), (350, 153), (450, 153), (550, 153), (650, 153), (750, 153),
                                    (150, 210), (250, 210), (350, 210), (450, 210), (550, 210), (650, 210), (750, 210),
                                    (100, 239), (200, 239), (300, 239), (398, 239), (498, 239), (598, 239), (698, 239), (800, 239),
                                    (100, 297), (200, 297), (300, 297), (398, 297), (498, 297), (598, 297), (698, 297), (800, 297),
                                    (46, 324), (146, 324), (246, 324), (346, 324), (446, 324), (546, 324), (646, 324), (746, 324), (850, 324),
                                    (46, 382), (146, 382), (246, 382), (346, 382), (446, 382), (546, 382), (646, 382), (746, 382), (846, 382),
                                    (94, 411), (194, 411), (294, 411), (394, 411), (494, 411), (594, 411), (696, 411), (794, 411),
                                    (94, 469), (194, 469), (294, 469), (394, 469), (494, 469), (594, 469), (696, 469), (794, 469),
                                    (144, 496), (244, 496), (344, 496), (444, 496), (544, 496), (644, 496), (744, 496),
                                    (144, 554), (244, 554), (344, 554), (444, 554), (544, 554), (644, 554), (744, 554),
                                    (194, 583), (294, 583), (394, 583), (494, 583), (594, 583), (694, 583),
                                    (194, 639), (294, 641), (394, 641), (494, 641), (594, 641), (694, 641),
                                    (243, 667), (343, 667), (443, 667), (543, 667), (643, 667)]]
port_game_degrees30 = [0, 2, 4, 6, 8, 16, 18, 20, 22, 24, 26, 35, 37, 39, 41, 43, 45, 47, 57, 59, 61, 63, 65, 67, 69, 71,
                       ]
ports_games_kinds = ["3:1" for _ in range(5)] + ["bricks", "iron", "wood", "wool", "wheat"]
ports_games_degrees = [30, -30, 90, -90, 150, -150]


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
        self.has_is_port = False

    def get_number(self):
        return self.number

    def __repr__(self):
        return f"TerrainTile1:({self.terrain_kind}, {self.placement}, {self.number}, {self.index})"

    def draw_tile(self, canvas):
        canvas.create_image(self.placement[0], self.placement[1], image=self.image_photo)
        if self.terrain_kind != "sea":
            canvas.create_image(self.placement[0], self.placement[1], image=self.place_numbers_image)
            canvas.create_image(self.placement[0], self.placement[1], image=self.number_photo)
        # canvas.create_text(self.placement[0], self.placement[1], text=self.index)

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
        self.ports = []

    def start(self):
        self.canvas.pack(side=tk.LEFT)
        self.canvas["height"] = self.root.winfo_screenheight()
        self.generate_map()
        self.draw_map()

    def draw_map(self):
        for index, tile in enumerate(self.tiles):
            tile.draw_tile(self.canvas)
        # for index in range(len(self.tiles)):
            # for index1, middle in enumerate(placements_middle_hexes_vertex_hexes[index][0]):
            #     self.canvas.create_text(middle[0], middle[1], text=str(index1))
            # for index1, vertex in enumerate(placements_middle_hexes_vertex_hexes[index][1]):
            #     self.canvas.create_text(vertex[0], vertex[1], text=str(index1))
        # for index1, placement1 in enumerate(placements_parts_builds_in_game[0]):
        #     self.canvas.create_text(placement1[0], placement1[1], text=str(index1))
        # for index1, placement1 in enumerate(placements_parts_builds_in_game[0]):
        #     self.canvas.create_text(placement1[0], placement1[1], text=str(index1))
        for index1, port in enumerate(self.ports):
            port.draw_port(self.canvas)

    def generate_map(self):
        tiles_count_copy = tiles_count[:]
        numbers_copy = numbers[:]
        print(len(tiles_count_copy), len(numbers_copy), len(tiles_count), len(numbers))  # not to delete
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
        ports_games_kinds_copy = ports_games_kinds[:]
        for _ in range(10):
            tiles_count_copy = []
            for index, tile in enumerate(self.tiles):
                if tile.terrain_kind != "sea":
                    list1 = []
                    for index1, placement in enumerate(forbidden_placements[index]):
                        if placement is not None and self.tiles[placement].terrain_kind == "sea" and not self.tiles[placement].has_is_port and not tile.has_is_port:
                            list1.append(index1)
                    if list1 is not None and list1 != []:
                        tiles_count_copy.append((tile, list1))  # [(tile, list1)]
            if tiles_count_copy is None or tiles_count_copy == []:  # in case that there are not enough shores and beaches (sea near land) in the map, the generator will give up generating placements and ports
                break
            tile_temp = random.choice(tiles_count_copy)
            print(tile_temp)
            placement_for_the_port = random.choice(tile_temp[1])
            print(placement_for_the_port)
            self.tiles[forbidden_placements[tile_temp[0].index][placement_for_the_port]].has_is_port = True
            self.tiles[tile_temp[0].index].has_is_port = True
            tiles_count_copy.remove(tile_temp)
            placement1 = placements_middle_hexes_vertex_hexes[tile_temp[0].index][0][placement_for_the_port]
            kind_of_the_port = random.choice(ports_games_kinds_copy)
            ports_games_kinds_copy.remove(kind_of_the_port)
            port1 = PortGame(placement_for_the_port, kind_of_the_port, placement1, ports_games_degrees[placement_for_the_port], tile_temp)
            self.ports.append(port1)

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
        self.note_book_players = ttk.Notebook(self.root, width=self.root.winfo_screenwidth() - 900, padding="0.05i",
                                              style="TNotebook")
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
        lbl4 = tk.Label(frame, text="number of roads and boats: 5", font="Arial 15", bg="#2596be")
        lbl5 = tk.Label(frame, text="number of knights used: 2", font="Arial 15", bg="#2596be")
        self.list_of_contents.append(frame)
        self.list_of_contents.append(lbl0)
        self.list_of_contents.append(lbl1)
        self.list_of_contents.append(lbl2)
        self.list_of_contents.append(lbl3)
        self.list_of_contents.append(lbl4)
        self.list_of_contents.append(lbl5)
        frame.pack(fill="both", expand=True)
        lbl0.pack(padx=10, pady=10, anchor=tk.NW)
        lbl1.pack(padx=10, pady=5, anchor=tk.NW)
        lbl2.pack(padx=10, pady=5, anchor=tk.NW)
        lbl3.pack(padx=10, pady=5, anchor=tk.NW)
        lbl4.pack(padx=10, pady=5, anchor=tk.NW)
        lbl5.pack(padx=10, pady=5, anchor=tk.NW)
        self.note_book_players.add(frame, text=name)

    def number_of_notes(self):
        return self.note_book_players.index("end") + 1  # the number of the last index + 1 I think

    def names_of_the_tabs(self):
        return self.note_book_players.tabs()

    def change_notes(self, list1):
        for index, content in list1:
            self.list_of_contents[index] = content


class PortGame(object):
    def __init__(self, index, port_kind, placement, degree_rotate_to, on_tile):
        self.index = index
        self.port_kind = port_kind
        self.placement = placement
        self.image_port_game_path = None
        self.degree_rotate_to = degree_rotate_to
        if self.port_kind != "3:1":
            self.image_port_game_path = fr"assets\catan_port_21_{self.port_kind}4.png"
        else:
            self.image_port_game_path = fr"assets\catan_port_31__6.png"
        self.image_port_game_path_image = Image.open(self.image_port_game_path).convert("RGBA")
        self.image_port_game_path_image = self.image_port_game_path_image.resize((84, 84), PIL.Image.Resampling.LANCZOS)
        self.image_port_game_path_image = self.image_port_game_path_image.rotate(self.degree_rotate_to)
        self.image_port_game_path_image = ImageTk.PhotoImage(self.image_port_game_path_image)
        self.on_tile = on_tile

    def draw_port(self, canvas):
        canvas.create_image(self.placement[0], self.placement[1], image=self.image_port_game_path_image)

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
    button_buy_road = tk.Button(root, text="Buy Road", relief="solid", font="Arial 15", bg="SkyBlue3",
                                activebackground="SkyBlue2")
    button_buy_boat = tk.Button(root, text="Buy Boat", relief="solid", font="Arial 15", bg="SkyBlue3",
                                activebackground="SkyBlue2")
    button_buy_settlement = tk.Button(root, text="Buy Settlement", relief="solid", font="Arial 15", bg="SkyBlue3",
                                      activebackground="SkyBlue2")
    button_buy_city = tk.Button(root, text="Buy City", relief="solid", font="Arial 15", bg="SkyBlue3",
                                activebackground="SkyBlue2")
    button_buy_development_card = tk.Button(root, text="Buy Development Card", relief="solid", font="Arial 15",
                                            bg="SkyBlue3", activebackground="SkyBlue2")
    button_declare_victory = tk.Button(root, text="Declare Victory", relief="solid", font="Arial 15", bg="SkyBlue3",
                                       activebackground="SkyBlue2")
    button_next_turn = tk.Button(root, text="Finished My Turn", relief="solid", font="Arial 15", bg="SkyBlue3",
                                 activebackground="SkyBlue2")
    button_buy_road.place(x=root.winfo_screenwidth() - 125, y=root.winfo_screenheight() - 400)
    button_buy_boat.place(x=root.winfo_screenwidth() - 250, y=root.winfo_screenheight() - 400)
    button_buy_settlement.place(x=root.winfo_screenwidth() - 430, y=root.winfo_screenheight() - 400)
    button_buy_city.place(x=root.winfo_screenwidth() - 112, y=root.winfo_screenheight() - 300)
    button_buy_development_card.place(x=root.winfo_screenwidth() - 352, y=root.winfo_screenheight() - 300)
    button_declare_victory.place(x=root.winfo_screenwidth() - 174, y=root.winfo_screenheight() - 200)
    button_next_turn.place(x=root.winfo_screenwidth() - 367, y=root.winfo_screenheight() - 200)
    root.mainloop()
