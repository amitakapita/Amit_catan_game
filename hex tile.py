import tkinter as tk
from PIL import Image, ImageTk
import PIL
import random
from tkinter import ttk
from typing import Type

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
forbidden_placements = [(None, None, None, 1, 5, 6), (None, None, 0, 2, 6, 7), (None, None, 1, 3, 7, 8),
                        (None, None, 2, 4, 8, 9), (None, None, 3, None, 9, 10),
                        (None, 0, None, 6, 11, 12), (0, 1, 5, 7, 12, 13), (1, 2, 6, 8, 13, 14), (2, 3, 7, 9, 14, 15),
                        (3, 4, 8, 10, 15, 16), (4, None, 9, None, 16, 17), (None, 5, None, 12, 18, 19),
                        (5, 6, 11, 13, 19, 20),
                        (6, 7, 12, 14, 20, 21), (7, 8, 13, 15, 21, 22), (8, 9, 14, 16, 22, 23), (9, 10, 15, 17, 23, 24),
                        (10, None, 16, None, 24, 25), (None, 11, None, 19, None, 26), (11, 12, 18, 20, 26, 27),
                        (12, 13, 19, 21, 27, 28),
                        (13, 14, 20, 22, 28, 29),
                        (14, 15, 21, 23, 29, 30), (15, 16, 22, 24, 30, 31), (16, 17, 23, 25, 31, 32),
                        (17, None, 24, None, 32, None),
                        (18, 19, None, 27, None, 33), (19, 20, 26, 28, 33, 34), (20, 21, 27, 29, 34, 35),
                        (21, 22, 28, 30, 35, 36),
                        (22, 23, 29, 31, 36, 37), (23, 24, 30, 32, 37, 38), (24, 25, None, 31, None, 38),
                        (26, 27, None, 34, None, 39),
                        (27, 28, 33, 35, 39, 40), (28, 29, 34, 36, 40, 41),
                        (29, 30, 35, 37, 41, 42), (30, 31, 36, 38, 42, 43), (31, 32, 37, None, 43, None),
                        (33, 34, None, 40, None, None),
                        (34, 35, 39, 41), (35, 36, 40, 42), (36, 37, 41, 43), (37, 38, 42, None, None, None)]
place_numbers_path = r"assets\place_numbers.png"
place_numbers_image = Image.open(place_numbers_path)
numbers_path = r"assets\numbers2.png"
numbers1_image = Image.open(numbers_path)
colors = ["firebrick4", "SteelBlue4", "chartreuse4", "#DBB600"]
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
placements_parts_builds_in_game = [
    [(220, 53), (280, 53), (320, 53), (380, 53), (420, 53), (480, 53), (520, 53), (580, 53), (620, 53), (680, 53),
     (199, 95), (301, 95), (401, 95), (501, 95), (601, 95), (701, 95),
     (170, 137), (220, 137), (280, 137), (320, 137), (380, 137), (420, 137), (480, 137), (520, 137), (580, 137),
     (620, 137), (680, 137), (720, 137),
     (148, 181), (250, 181), (350, 181), (450, 181), (550, 181), (650, 181), (750, 181),
     (118, 225), (178, 225), (218, 225), (278, 225), (318, 225), (378, 225), (418, 225), (478, 225), (518, 225),
     (578, 225), (618, 225), (678, 225), (718, 225), (768, 225),
     (97, 267), (197, 267), (297, 267), (397, 267), (497, 267), (597, 267), (697, 267), (797, 267),
     (69, 309), (129, 309), (169, 309), (229, 309), (269, 309), (329, 309), (369, 309), (420, 309), (480, 309),
     (520, 309), (580, 309), (620, 309), (680, 309), (720, 309), (780, 309), (820, 309),
     (46, 353), (146, 353), (246, 353), (346, 353), (446, 353), (546, 353), (646, 353), (746, 353), (846, 353),
     (69, 395), (129, 395), (169, 395), (229, 395), (269, 395), (329, 395), (369, 395), (420, 395), (480, 395),
     (520, 395), (580, 395), (620, 395), (680, 395), (720, 395), (780, 395), (820, 395),
     (97, 439), (197, 439), (297, 439), (397, 439), (497, 439), (597, 439), (697, 439), (797, 439),
     (118, 481), (178, 481), (218, 481), (278, 481), (318, 481), (378, 481), (418, 481), (478, 481), (518, 481),
     (578, 481), (618, 481), (678, 481), (718, 481), (768, 481),
     (148, 525), (250, 525), (350, 525), (450, 525), (550, 525), (650, 525), (750, 525),
     (170, 567), (220, 567), (280, 567), (320, 567), (380, 567), (420, 567), (480, 567), (520, 567), (580, 567),
     (620, 567), (680, 567), (720, 567),
     (199, 611), (301, 611), (401, 611), (501, 611), (601, 611), (701, 611),
     (220, 653), (280, 653), (320, 653), (380, 653), (420, 653), (480, 653), (520, 653), (580, 653), (620, 653),
     (680, 653)],
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
port_game_degrees30 = [0, 2, 4, 6, 8, 16, 18, 20, 22, 24, 26, 35, 37, 39, 41, 43, 45, 47, 57, 59, 61, 63, 65, 67, 69,
                       71,
                       ]
ports_games_kinds = ["3:1" for _ in range(5)] + ["bricks", "iron", "wood", "wool", "wheat"]
ports_games_degrees = [30, -30, 90, -90, 150, -150]
forbidden_placements_parts_in_the_game = [(5, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 0)]
what_part_is_on_what_tile_hex = [[(None, 0), (None, 0), (None, 1), (None, 1), (None, 2), (None, 2), (None, 3), (None, 3), (None, 4), (None, 4),
                                  (None, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, None),
                                  (None, 5), (0, 5), (0, 6), (1, 6), (1, 7), (2, 7), (2, 8), (3, 8), (3, 9), (4, 9), (4, 10), (10, None),
                                  (None, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, None),
                                  (None, 11), (5, 11), (5, 12), (6, 12), (6, 13), (7, 13), (7, 14), (8, 14), (8, 15), (9, 15), (9, 16), (10, 16), (10, 17), (17, None),
                                  (None, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, None),
                                  (None, 18), (11, 18), (11, 19), (12, 19), (12, 20), (13, 20), (13, 21), (14, 21), (14, 22), (15, 22), (15, 23), (16, 23), (16, 24), (17, 24), (17, 25), (25, None),
                                  (None, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, None),
                                  (None, 18), (18, 26), (19, 26), (19, 27), (20, 27), (20, 28), (21, 28), (21, 29), (22, 29), (22, 30), (23, 30), (23, 31), (24, 31), (24, 32), (25, 32), (32, None),
                                  (None, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 32), (32, None),
                                  (None, 26), (26, 33), (27, 33), (27, 34), (28, 34), (28, 35), (29, 35), (29, 36), (30, 36), (30, 37), (31, 37), (31, 38), (32, 38), (32, None),
                                  (None, 33), (33, 34), (34, 35), (35, 36), (36, 37), (37, 38), (38, None),
                                  (None, 33), (33, 39), (34, 39), (34, 40), (35, 40), (35, 41), (36, 41), (36, 42), (37, 42), (37, 43), (38, 43), (38, None),
                                  (None, 39), (39, 40), (40, 41), (41, 42), (42, 43), (43, None),
                                  (39, None), (39, None), (40, None), (40, None), (41, None), (41, None), (42, None), (42, None), (43, None), (43, None)],
                                 [(None, None, 0), (None, None, 1), (None, None, 2), (None, None, 3), (None, None, 4),
                                  (None, None, 0), (None, 0, 1), (None, 1, 2), (None, 2, 3), (None, 3, 4), (None, 4, None),
                                  (None, 0, 5), (0, 1, 6), (1, 2, 7), (2, 3, 8), (3, 4, 9), (4, None, 10),
                                  (None, None, 5), (0, 5, 6), (1, 6, 7), (2, 7, 8), (3, 8, 9), (4, 9, 10), (None, 10, None),
                                  (None, 5, 11), (5, 6, 12), (6, 7, 13), (7, 8, 14), (8, 9, 15), (9, 10, 16), (10, None, 17),
                                  (None, None, 11), (5, 11, 12), (6, 12, 13), (7, 13, 14), (8, 14, 15), (9, 15, 16), (10, 16, 17), (None, 17, None),
                                  (None, 11, 18), (11, 12, 19), (12, 13, 20), (13, 14, 21), (14, 15, 22), (15, 16, 23), (16, 17, 24), (17, None, 25),
                                  (None, None, 18), (11, 18, 19), (12, 18, 20), (13, 20, 21), (14, 21, 22), (15, 22, 23), (16, 23, 24), (17, 24, 25), (None, 25, None),
                                  (None, 18, None), (18, 19, 26), (19, 20, 27), (20, 21, 28), (21, 22, 29), (22, 23, 30), (23, 24, 31), (24, 25, 32), (25, None, None),
                                  (18, None, 26), (19, 26, 27), (20, 27, 28), (21, 28, 29), (22, 29, 30), (23, 30, 31), (24, 31, 32), (25, 32, None),
                                  (None, 26, None), (26, 27, 33), (27, 28, 34), (28, 29, 35), (29, 30, 36), (30, 31, 37), (31, 32, 38), (32, None, None),
                                  (26, None, 33), (27, 33, 34), (28, 34, 35), (29, 35, 36), (30, 36, 37), (31, 37, 38), (32, 38, None),
                                  (None, 33, None), (33, 34, 39), (34, 35, 40), (35, 36, 41), (36, 37, 42), (37, 38, 43), (38, None, None),
                                  (33, None, 39), (34, 39, 40), (35, 40, 41), (36, 41, 42), (37, 42, 43), (38, 43, None),
                                  (None, 39, None), (39, 40, None), (40, 41, None), (41, 42, None), (42, 43, None), (43, None, None),
                                  (39, None, None), (40, None, None), (41, None, None), (42, None, None), (43, None, None)]]
places_in_each_placements_for_the_hexes = [[(None, 5),
                                            (None, 0),
                                            (None, 5),
                                            (None, 0),
                                            (None, 5),
                                            (None, 0),
                                            (None, 5),
                                            (None, 0),
                                            (None, 5),
                                            (None, 0),
                                            (None, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, None),
                                            (None, 5),
                                            (3, 0),
                                            (2, 5), (3, 0),
                                            (2, 5), (3, 0),
                                            (2, 5), (3, 0),
                                            (2, 5), (3, 0),
                                            (2, 5), (None, 0),
                                            (None, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, None),
                                            (None, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (None, 0),
                                            (None, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, None),
                                            (None, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (None, 0),
                                            (None, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, None),
                                            (3, None),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, None),
                                            (None, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, None),
                                            (3, None),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, None),
                                            (None, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, None),
                                            (3, None),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, 5),
                                            (3, 0),
                                            (2, None),
                                            (None, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, 4),
                                            (1, None),
                                            (3, None), (2, None),
                                            (3, None), (2, None),
                                            (3, None), (2, None),
                                            (3, None), (2, None),
                                            (3, None), (2, None)], [(None, None, 0),
                                                (None, None, 0),
                                                (None, None, 0),
                                                (None, None, 0),
                                                (None, None, 0),
                                                (None, None, 5),
                                                (None, 1, 5),
                                                (None, 1, 5),
                                                (None, 1, 5),
                                                (None, 1, 5),
                                                (None, 1, None),
                                                (None, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, None, 0),
                                                (None, None, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (None, 1, None),
                                                (None, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, None, 0),
                                                (None, None, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (None, 1, None),
                                                (None, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, None, 0),
                                                (None, None, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (None, 1, None),
                                                (None, 4, None),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, None, None),
                                                (3, None, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, None),
                                                (None, 4, None),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, None, None),
                                                (3, None, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (2, None, None),
                                                (None, 4, None),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, 4, 0),
                                                (2, None, None),
                                                (3, None, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, 5),
                                                (3, 1, None),
                                                (None, 4, None),
                                                (2, 4, None),
                                                (2, 4, None),
                                                (2, 4, None),
                                                (2, 4, None),
                                                (2, None, None),
                                                (3, None, None),
                                                (3, None, None),
                                                (3, None, None),
                                                (3, None, None),
                                                (3, None, None)]]
indexes_roads_xyx1y1_positions = [(155, 160), (155, 161), (156, 161), (156, 162), (157, 162), (157, 163), (158, 163), (158, 164), (159, 164), (159, 165),
                                  (160, 166), (161, 167), (162, 168), (163, 169), (164, 170), (165, 171),
                                  (166, 172), (166, 173), (167, 173), (167, 174), (168, 174), (168, 175), (169, 175), (169, 176), (170, 176), (170, 177), (171, 177), (171, 178),
                                  (172, 179), (173, 180), (174, 181), (175, 182), (176, 183), (177, 184), (178, 185),
                                  (179, 186), (179, 187), (180, 187), (180, 188), (181, 188), (181, 189), (182, 189), (182, 190), (183, 190), (183, 191), (184, 191), (184, 192), (185, 192), (185, 193),
                                  (186, 194), (187, 195), (188, 196), (189, 197), (190, 198), (191, 199), (192, 200), (193, 201),
                                  (202, 194), (194, 203), (195, 203), (195, 204), (196, 204), (196, 205), (197, 205), (197, 206), (198, 206), (198, 207), (199, 207), (199, 208), (200, 208), (200, 209), (201, 209), (201, 210),
                                  (202, 211), (203, 212), (204, 213), (205, 214), (206, 215), (207, 216), (208, 217), (209, 218), (210, 219),
                                  (211, 220), (212, 220), (212, 221), (213, 221), (213, 222), (214, 222), (214, 223), (215, 223), (215, 224), (216, 224), (216, 225), (217, 225), (217, 226), (218, 226), (218, 227), (219, 227),
                                  (220, 228), (221, 229), (222, 230), (223, 231), (224, 232), (225, 233), (226, 234), (227, 235),
                                  (228, 236), (229, 236), (229, 237), (230, 237), (230, 238), (231, 238), (231, 239), (232, 239), (232, 240), (233, 240), (233, 241), (234, 241), (234, 242), (235, 242),
                                  (236, 243), (237, 244), (238, 245), (239, 246), (240, 247), (241, 248), (242, 249),
                                  (243, 250), (244, 250), (244, 251), (245, 251), (245, 252), (246, 252), (246, 253), (247, 253), (247, 254), (248, 254), (248, 255), (249, 255),
                                  (250, 256), (251, 257), (252, 258), (253, 259), (254, 260), (255, 261),
                                  (256, 262), (257, 262), (257, 263), (258, 263), (258, 264), (259, 264), (259, 265), (260, 265), (260, 266), (261, 266)]
near_road_boat_numbers_indexes = [(1, 10), (0, 2, 11), (1, 3, 11), (2, 4, 12), (3, 5, 12), (4, 6, 13), (5, 7, 13), (6, 8, 14), (7, 9, 14), (8, 15),
                                  (10, 16, 17), (1, 2, 18, 19), (3, 4, 20, 21), (5, 6, 22, 23), (7, 8, 24, 25), (9, 26, 27),
                                  (10, 17, 28), (10, 16, 18, 29), (11, 17, 19, 29), (11, 18, 20, 30), (12, 19, 21, 30), (12, 20, 22, 31), (13, 21, 23, 31), (13, 22, 24, 32), (14, 23, 25, 32), (14, 24, 26, 33), (15, 25, 27, 33), (15, 26, 34),
                                  (16, 35, 36), (17, 18, 37, 38), (19, 20, 39, 40), (21, 22, 41, 42), (23, 24, 43, 44), (25, 26, 45, 46), (27, 47, 48),
                                  (28, 36, 49), (28, 35, 37, 50), (29, 36, 38, 50), (29, 37, 39, 51), (30, 38, 40, 51), (30, 39, 41, 52), (31, 40, 42, 52), (31, 41, 43, 53), (32, 42, 44, 53), (32, 43, 45, 54), (33, 44, 46, 54), (33, 45, 47, 55), (34, 46, 48, 55), (34, 47, 56),
                                  (35, 57, 58), (36, 37, 59, 60), (38, 39, 61, 62), (40, 41, 63, 64), (42, 43, 65, 66), (44, 45, 67, 68), (46, 47, 69, 70), (48, 71, 72),
                                  (39, 58, 73), (49, 57, 59, 74), (50, 58, 60, 74), (50, 59, 61, 75), (51, 60, 62, 75), (51, 61, 63, 76), (52, 62, 64, 76), (52, 63, 65, 77), (53, 64, 66, 77), (53, 65, 67, 78), (54, 66, 68, 78), (54, 67, 69, 79), (55, 68, 70, 79), (55, 69, 71, 80), (56, 70, 72, 80), (56, 71, 81),
                                  (57, 82), (58, 59, 83, 84), (60, 61, 85, 86), (62, 63, 87, 88), (64, 65, 89, 90), (66, 67, 91, 92), (68, 69, 93, 94), (70, 71, 95, 96), (72, 97),
                                  (73, 83, 98), (74, 82, 84, 98), (74, 83, 85, 99), (75, 84, 86, 99), (75, 85, 87, 100), (76, 86, 88, 100), (76, 87, 89, 101), (77, 88, 90, 101), (77, 89, 91, 102), (78, 90, 92, 102), (78, 91, 93, 103), (79, 92, 94, 103), (79, 93, 95, 104), (80, 94, 96, 104), (80, 95, 97, 105), (81, 96, 105),
                                  (82, 83, 106), (84, 85, 107, 108), (86, 87, 109, 110), (88, 89, 111, 112), (90, 91, 113, 114), (92, 93, 115, 116), (94, 95, 117, 118), (96, 97, 119),
                                  (98, 107, 120), (99, 106, 108, 120), (99, 107, 109, 121), (100, 108, 110, 121), (100, 109, 111, 122), (101, 110, 112, 122), (101, 111, 113, 123), (102, 112, 114, 123), (102, 1113, 115, 124), (103, 114, 116, 124), (103, 115, 117, 125), (104, 116, 118, 125), (104, 117, 119, 126), (105, 118, 126),
                                  (106, 107, 127), (108, 109, 128, 129), (110, 111, 130, 131), (112, 113, 132, 133), (114, 115, 134, 135), (116, 117, 136, 137), (118, 119, 138),
                                  (120, 128, 139), (121, 127, 129, 139), (121, 128, 130, 140), (122, 129, 131, 140), (122, 130, 132, 141), (123, 131, 133, 141), (123, 132, 134, 142), (124, 133, 135, 142), (124, 134, 136, 143), (125, 135, 137, 143), (125, 136, 138, 144), (126, 137, 144),
                                  (127, 128, 145), (129, 130, 146, 147), (131, 132, 148, 149), (133, 134, 150, 151), (135, 136, 152, 153), (137, 138, 154),
                                  (139, 146), (140, 145, 147), (140, 146, 148), (141, 147, 149), (141, 148, 150), (142, 149, 151), (142, 150, 152), (143, 151, 153), (143, 152, 154), (144, 153)]


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
        self.parts_in_game = []
        self.forbidden_placements_in_tile = []
        self.roads_and_boats = []

    def get_number(self):
        return self.number

    def __repr__(self):
        return f"TerrainTile1:(terrain_kind:{self.terrain_kind}, placement:{self.placement}, number:{self.number}, index:{self.index}, parts_in_game:{self.parts_in_game}, forbidden_placements_in_tile:{self.forbidden_placements_in_tile}, roads_and_boats:{self.roads_and_boats})"

    def draw_tile(self, canvas):
        canvas.create_image(self.placement[0], self.placement[1], image=self.image_photo)
        if self.terrain_kind != "sea":
            canvas.create_image(self.placement[0], self.placement[1], image=self.place_numbers_image)
            canvas.create_image(self.placement[0], self.placement[1], image=self.number_photo)
        canvas.create_text(self.placement[0], self.placement[1], text=self.index)

    def change_photo_number(self):
        self.number_photo = numbers1_image.crop((0 + 40 * (self.number - 1) - 2, 0, 0 + 40 * self.number, 40))
        self.number_photo = self.number_photo.resize((30, 30), PIL.Image.Resampling.LANCZOS)
        self.number_photo = ImageTk.PhotoImage(self.number_photo)

    def add_building(self, building, index1, is_settlement_or_city=True):
        type_building = Type[type(building)]
        print(type_building, Type[Settlement], type_building == Type[Settlement])
        if is_settlement_or_city and type_building == Type[Settlement]:
            if index1 is not None:
                self.parts_in_game.append((index1, building))  # index - the index 0-5 (including) in the tile hex, building - the object of the building
                self.forbidden_placements_in_tile.append(forbidden_placements_parts_in_the_game[index1])
        elif type_building == Type[City]:
            self.parts_in_game.append((index1, building))
            self.forbidden_placements_in_tile.append(forbidden_placements_parts_in_the_game[index1])
        elif type_building == Type[Road]:
            if index1 is not None:
                self.roads_and_boats.append((index1, building))
                # self.parts_in_game.append((index1, building))
        elif type_building == Type[Boat]:
            if index1 is not None:
                self.roads_and_boats.append((index1, building))

    def check_validation_parts_in_the_game(self, wanted_settlement_or_city_index):
        return self.check_validation_placements_buildings(wanted_settlement_or_city_index)

    def check_validation_placements_buildings(self, index):
        for placement in self.forbidden_placements_in_tile:
            if index in placement:
                return False
        return True

    def delete_building(self, index1):
        for index2 in self.parts_in_game:
            if index2[0] == index1:
                self.parts_in_game.remove(index2)
                self.forbidden_placements_in_tile.remove(forbidden_placements_parts_in_the_game[index1])  # can build there
                break

    def delete_road_or_boat(self, index1):
        for index2 in self.roads_and_boats:
            if index2[0] == index1:
                self.roads_and_boats.remove(index2)
                break


class Map(object):
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.root, bg="#2596be", width=900, highlightbackground="black", highlightthickness=3)
        self.tiles = []
        self.ports = []
        self.Circle_choosing_image_path = r"assets\Circle_choosing1.png"
        self.Circle_choosing_photo_image = Image.open(self.Circle_choosing_image_path).convert("RGBA")
        self.Circle_choosing_photo_image = ImageTk.PhotoImage(self.Circle_choosing_photo_image)
        self.none_any_circle = ImageTk.PhotoImage(Image.open(r"assets\None_of_circles.png").convert("RGBA"))
        self.ids_placements = []
        self.current_button = None
        self.button_buy_road = tk.Button(root, text="Buy Road", relief="solid", font="Arial 15", bg="SkyBlue3",
                                         activebackground="SkyBlue2",
                                         command=lambda: self.change_current_button("road"))
        self.button_buy_boat = tk.Button(root, text="Buy Boat", relief="solid", font="Arial 15", bg="SkyBlue3",
                                         activebackground="SkyBlue2",
                                         command=lambda: self.change_current_button("boat"))
        self.button_buy_settlement = tk.Button(root, text="Buy Settlement", relief="solid", font="Arial 15",
                                               bg="SkyBlue3",
                                               activebackground="SkyBlue2",
                                               command=lambda: self.change_current_button("settlement"))
        self.button_buy_city = tk.Button(root, text="Buy City", relief="solid", font="Arial 15", bg="SkyBlue3",
                                         activebackground="SkyBlue2",
                                         command=lambda: self.change_current_button("city"))
        self.button_buy_development_card = tk.Button(root, text="Buy Development Card", relief="solid", font="Arial 15",
                                                     bg="SkyBlue3", activebackground="SkyBlue2",
                                                     command=lambda: self.change_current_button("development_card"))
        self.button_declare_victory = tk.Button(root, text="Declare Victory", relief="solid", font="Arial 15",
                                                bg="SkyBlue3",
                                                activebackground="SkyBlue2",
                                                command=lambda: self.change_current_button("declare_victory"))
        self.button_next_turn = tk.Button(root, text="Finished My Turn", relief="solid", font="Arial 15", bg="SkyBlue3",
                                          activebackground="SkyBlue2",
                                          command=lambda: self.change_current_button("next_turn"))
        self.where_place = tk.Label(self.root, text="Where to place?", bg="#2596be", font="Arial 15")
        self.place_entry = tk.Entry(self.root, bg="SkyBlue3", font="Arial 15")
        self.button_buy = tk.Button(self.root, bg="SkyBlue3", activebackground="SkyBlue2", font="Arial 15", text="Buy", relief="solid")
        self.image1 = Image.open(r"assets\Settlement_red.png").convert("RGBA")
        self.image1 = ImageTk.PhotoImage(self.image1)
        self.image2 = ImageTk.PhotoImage(Image.open(r"assets\Settlement_blue.png").convert("RGBA"))
        self.image3 = ImageTk.PhotoImage(Image.open(r"assets\Settlement_green.png").convert("RGBA"))
        self.image4 = ImageTk.PhotoImage(Image.open(r"assets\Settlement_yellow.png").convert("RGBA"))
        self.settlements = []  # (index, settlement)
        self.cities = []  # (index, city)
        self.image_city_red = ImageTk.PhotoImage(Image.open(r"assets/City_red.png").convert("RGBA"))
        self.image_city_blue = ImageTk.PhotoImage(Image.open(r"assets/City_blue.png").convert("RGBA"))
        self.image_city_green = ImageTk.PhotoImage(Image.open(r"assets/City_green.png").convert("RGBA"))
        self.image_city_yellow = ImageTk.PhotoImage(Image.open(r"assets/City_yellow.png").convert("RGBA"))
        self.roads = []
        self.cancel_buying_button = tk.Button(self.root, bg="SkyBlue3", activebackground="SkyBlue2", font="Arial 15", text="Cancel", relief="solid", command=self.close_placements)
        self.boats = []
        self.image_path_boat1 = fr"assets\Boat_red.png"
        self.image_boat_1 = ImageTk.PhotoImage(Image.open(self.image_path_boat1).convert("RGBA"))
        self.image_boat_2 = ImageTk.PhotoImage(Image.open(fr"assets\Boat_blue.png").convert("RGBA"))
        self.image_boat_3 = ImageTk.PhotoImage(Image.open(fr"assets\Boat_green.png").convert("RGBA"))
        self.image_boat_4 = ImageTk.PhotoImage(Image.open(fr"assets\Boat_yellow.png").convert("RGBA"))

    def start(self):
        self.canvas.pack(side=tk.LEFT)
        self.canvas["height"] = self.root.winfo_screenheight()
        self.generate_map()
        self.draw_map()
        for index, placement1 in enumerate(placements_parts_builds_in_game[0] + placements_parts_builds_in_game[1]):
            id_placement = self.canvas.create_image(placement1[0], placement1[1], image=self.none_any_circle,
                                                    activeimage=self.Circle_choosing_photo_image, tags="circle_tag")
            print(id_placement, end=", ")
            self.ids_placements.append(id_placement)
            i = self.canvas.create_text(placement1[0], placement1[1], text=str(index), state=tk.DISABLED, tags="indexes_texts_rectangles")
            r = self.canvas.create_rectangle(self.canvas.bbox(i), fill="#2596be", tags="indexes_texts_rectangles")
            self.canvas.itemconfigure(i, state=tk.HIDDEN)
            self.canvas.itemconfigure(r, state=tk.HIDDEN)
            self.canvas.tag_lower(r, i)
            # self.canvas.tag_bind(id_placement, "<Button-1>", lambda x: self.canvas.itemconfigure(self.canvas.find_withtag(), image=self.Circle_choosing_photo_image))
        self.button_buy_road.place(x=root.winfo_screenwidth() - 125, y=root.winfo_screenheight() - 420)
        self.button_buy_boat.place(x=root.winfo_screenwidth() - 250, y=root.winfo_screenheight() - 420)
        self.button_buy_settlement.place(x=root.winfo_screenwidth() - 430, y=root.winfo_screenheight() - 420)
        self.button_buy_city.place(x=root.winfo_screenwidth() - 112, y=root.winfo_screenheight() - 360)
        self.button_buy_development_card.place(x=root.winfo_screenwidth() - 352, y=root.winfo_screenheight() - 360)
        self.button_declare_victory.place(x=root.winfo_screenwidth() - 174, y=root.winfo_screenheight() - 300)
        self.button_next_turn.place(x=root.winfo_screenwidth() - 367, y=root.winfo_screenheight() - 300)
        self.button_buy["command"] = lambda: self.close_placements()
        # self.canvas.tag_lower("road", "settlement")
        # self.canvas.tag_lower("road", "city")


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
                        if placement is not None and self.tiles[placement].terrain_kind == "sea" and not self.tiles[
                            placement].has_is_port and not tile.has_is_port:
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
            port1 = PortGame(placement_for_the_port, kind_of_the_port, placement1,
                             ports_games_degrees[placement_for_the_port], tile_temp)
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
        return [tile.__repr__() for tile in self.tiles], [port.__repr__ for port in self.ports]

    def change_current_button(self, new_current):
        self.current_button = new_current
        self.place_entry.place(x=self.root.winfo_screenwidth() - 300, y=self.root.winfo_screenheight() - 200)
        self.button_buy.place(x=self.root.winfo_screenwidth() - 125, y=self.root.winfo_screenheight() - 150)
        self.where_place["text"] = f"Where to place your {self.current_button}?"
        self.where_place.place(x=self.root.winfo_screenwidth() - 300, y=self.root.winfo_screenheight() - 230)
        self.cancel_buying_button.place(x=self.root.winfo_screenwidth() - 300, y=self.root.winfo_screenheight() - 150)
        for item in self.canvas.find_withtag("indexes_texts_rectangles"):
            print(item, end=", ")  # not to delete
            self.canvas.itemconfigure(item, state=tk.DISABLED)

    def handle_buttons(self):
        position1 = self.place_entry.get()
        if position1 != "":
            for element in position1:
                if element not in "1234567890":
                    return "an index is in numbers"
            position1 = int(position1)
            if 0 <= position1 <= 154:
                if self.current_button == "road":
                    # if there is not there any road, and there is a the player's settlement or city near, or there is a road of the player near
                    if self.checking_city_or_settlement_is_near_the_road(position1, "red") or self.checking_roads_or_boats_is_near_the_road(position1, "red"):
                        road = Road(index=position1, color="red", position=indexes_roads_xyx1y1_positions[position1])
                        road.draw_road(self.canvas)
                        self.roads.append((position1, road))
                        for tile in what_part_is_on_what_tile_hex[0][position1]:
                            if tile is not None:
                                tile = self.tiles[tile]
                                tile.add_building(road, places_in_each_placements_for_the_hexes[0][position1], is_settlement_or_city=False)
                                print(tile)
                        self.canvas.tag_lower("road", "settlement")  # that for the assuming that roads are built after placing settlements and over and more
                elif self.current_button == "boat":
                    if self.checking_boats_is_near_a_settlement_or_city(position1, "red") or self.checking_boats_is_near_the_road_or_a_boat(position1, "red"):
                        boat = Boat(index=position1, color="red", position=(indexes_roads_xyx1y1_positions[position1]), image1=self.image_boat_1)
                        boat.draw_boat(self.canvas)
                        self.boats.append((position1, boat))
                        for tile in what_part_is_on_what_tile_hex[0][position1]:
                            if tile is not None:
                                tile = self.tiles[tile]
                                tile.add_building(boat, places_in_each_placements_for_the_hexes[0][position1], is_settlement_or_city=False)
                                print(tile)
                        self.canvas.tag_lower("boat", "settlement")  # that for the assuming that roads are built after placing settlements and over and more
                        # and in order to see the boat's image
                        self.canvas.tag_lower("road", "boat")
            elif 267 > position1 > 154:
                if self.current_button == "city":
                    for index, settlement in self.settlements:
                        if index == position1 and settlement.color == "red":
                            self.canvas.delete(settlement.id)
                            self.settlements.remove((index, settlement))
                            city1 = City(color="red", index=position1, position=(placements_parts_builds_in_game[0] + placements_parts_builds_in_game[1])[int(position1)], img=self.image_city_red)
                            print(city1)  # not to delete
                            city1.draw_city(self.canvas)
                            print(city1)  # not to delete
                            self.cities.append((position1, city1))
                            for index2, tile_index in enumerate([index for index in what_part_is_on_what_tile_hex[1][position1 - 155]]):
                                if tile_index is not None:
                                    tile_index1 = self.tiles[tile_index]
                                    tile_index1.delete_building(places_in_each_placements_for_the_hexes[1][position1 - 155][index2])
                                    tile_index1.add_building(city1, places_in_each_placements_for_the_hexes[1][position1 - 155][index2], is_settlement_or_city=False)
                                    print(index2, tile_index1, tile_index)
                            print(self.settlements)
                            print(self.cities)
                            return True
                    return False
                elif self.current_button == "settlement":
                    if self.checking_settlement(position1, "red"):
                        settlement1 = Settlement(color="red", index=int(position1), position=(placements_parts_builds_in_game[0] + placements_parts_builds_in_game[1])[int(position1)], img=self.image1)
                        print(settlement1)
                        settlement1.draw_settlement(self.canvas)
                        index2 = 0
                        for index1 in [index for index in what_part_is_on_what_tile_hex[1][position1 - 155]]:
                            if index1 is not None:
                                tile = self.tiles[index1]
                                print(tile, index1)
                                tile.add_building(building=settlement1, index1=places_in_each_placements_for_the_hexes[1][position1 - 155][index2], is_settlement_or_city=True)
                            index2 += 1
                        self.settlements.append((position1, settlement1))
                        return True


    def close_placements(self):
        self.place_entry.place_forget()
        self.button_buy.place_forget()
        self.cancel_buying_button.place_forget()
        self.where_place.place_forget()
        for item in self.canvas.find_withtag("indexes_texts_rectangles"):
            print(item, end=", ")  # not to delete
            self.canvas.itemconfigure(item, state=tk.HIDDEN)
        self.handle_buttons()

    def checking_city_or_settlement_is_near_the_road(self, index_road, color):
        for index_road1 in self.roads:  # there is already a road there
            if index_road1[0] == index_road:
                return False
        for index_boat1 in self.boats:  # there is already a boat
            if index_boat1[0] == index_road:
                return False
        counter_none_and_sea_tiles = 0
        print(what_part_is_on_what_tile_hex[0][index_road])
        for tile in what_part_is_on_what_tile_hex[0][index_road]:
            if tile is None or self.tiles[tile].terrain_kind == "sea":
                counter_none_and_sea_tiles += 1
        if counter_none_and_sea_tiles >= 2:
            return False
        for placement in indexes_roads_xyx1y1_positions[index_road]:
            for index_settlement in self.settlements:  # a settlement is near the road
                if index_settlement[0] == placement and index_settlement[1].color == color:
                    return True
            for index_city in self.cities:  # a city is near the road
                if index_city[0] == placement and index_city[1].color == color:
                    return True
        return False  # none of them

    def checking_roads_or_boats_is_near_the_road(self, index_road, color):
        for index_road1 in self.roads:  # there is already a road there
            if index_road1[0] == index_road:
                return False
        for index_boat1 in self.boats:  # there is already a boat
            if index_boat1[0] == index_road:
                return False
        counter_none_and_sea_tiles = 0
        for tile in what_part_is_on_what_tile_hex[0][index_road]:
            if tile is None or self.tiles[tile].terrain_kind == "sea":
                counter_none_and_sea_tiles += 1
        if counter_none_and_sea_tiles >= 2:
            return False
        for placement in near_road_boat_numbers_indexes[index_road]:  # a road is near the placement that is of the player or a boat is near the placement that is of the player
            for index_road1 in self.roads:
                if index_road1[0] == placement and index_road1[1].color == color:
                    return True
            for index_boat1 in self.boats:
                if index_boat1[0] == placement and index_boat1[1].color == color:
                    return True
        return False

    def checking_settlement(self, position, color):
        for index_settlement in self.settlements:  # if there is already a settlement or a city in this index
            if index_settlement[0] == position:
                return False
        for index_city in self.cities:  # about the city if there is already a settlement or a city in this index
            if index_city[0] == position:
                return False
        counter_sea_tiles_and_Nones = 0
        for index3, tile in enumerate([index for index in what_part_is_on_what_tile_hex[1][position - 155]]):  # if there is not only seas or Nones
            if tile is None or self.tiles[tile].terrain_kind == "sea":
                counter_sea_tiles_and_Nones += 1
                print(counter_sea_tiles_and_Nones, tile)
                continue
            tile = self.tiles[tile]
            print(f"\n{tile}\n{places_in_each_placements_for_the_hexes[1][position - 155][index3]}\n{tile.check_validation_parts_in_the_game(places_in_each_placements_for_the_hexes[1][position - 155][index3])}\n{counter_sea_tiles_and_Nones}")
            if not tile.check_validation_parts_in_the_game(places_in_each_placements_for_the_hexes[1][position - 155][index3]):  # fi it's valid from the fact that it can be only after 2 roads and that
                return False
        if counter_sea_tiles_and_Nones >= 3:
            return False
        return True

    def checking_boats_is_near_the_road_or_a_boat(self, index_boat, color):
        for index_boat1 in self.boats:  # there is there a road
            if index_boat1[0] == index_boat:
                return False
        for index_road1 in self.roads:  # there is there a boat
            if index_road1[0] == index_boat:
                return False
        counter_none_and_sea_tiles = 0
        print(what_part_is_on_what_tile_hex[0][index_boat])
        for tile in what_part_is_on_what_tile_hex[0][index_boat]:
            if tile is None or self.tiles[tile].terrain_kind == "sea":
                counter_none_and_sea_tiles += 1
        if counter_none_and_sea_tiles == 0:  # only land
            return False
        for placement in near_road_boat_numbers_indexes[index_boat]:  # a road is near the placement that is of the player or a boat is near the placement that is of the player
            for index_road1 in self.roads:
                if index_road1[0] == placement and index_road1[1].color == color:
                    return True
            for index_boat1 in self.boats:
                if index_boat1[0] == placement and index_boat1[1].color == color:
                    return True
        return False

    def checking_boats_is_near_a_settlement_or_city(self, index_boat, color):
        for index_road1 in self.roads:  # there is already a road there
            if index_road1[0] == index_boat:
                return False
        for index_boat1 in self.boats:  # there is already a boat
            if index_boat1[0] == index_boat:
                return False
        counter_none_and_sea_tiles = 0
        print(what_part_is_on_what_tile_hex[0][index_boat])
        for tile in what_part_is_on_what_tile_hex[0][index_boat]:
            if tile is None or self.tiles[tile].terrain_kind == "sea":
                counter_none_and_sea_tiles += 1
        if counter_none_and_sea_tiles == 0:
            return False
        for placement in indexes_roads_xyx1y1_positions[index_boat]:
            for index_settlement in self.settlements:  # a settlement is near the road
                if index_settlement[0] == placement and index_settlement[1].color == color:
                    return True
            for index_city in self.cities:  # a city is near the road
                if index_city[0] == placement and index_city[1].color == color:
                    return True
        return False  # none of them



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

    def __repr__(self):
        return f"PortGame:({self.index}, {self.port_kind}, {self.placement}, {self.on_tile})"


class Settlement(object):
    def __init__(self, color, index, position, img):
        self.color = color
        self.index = index
        self.position = position
        self.img = img
        self.id = None

    def draw_settlement(self, canvas):
        self.id = canvas.create_image(self.position[0], self.position[1], image=self.img, tags=("red_settlement", "settlement"))
        return self.id

    def __repr__(self):
        return f"Settlement:(color:{self.color}, index:{self.index}, position:{self.position}, id:{self.id})"


class City(object):
    def __init__(self, color, index, position, img):
        self.color = color
        self.index = index
        self.position = position
        self.img = img
        self.id = None

    def draw_city(self, canvas):
        self.id = canvas.create_image(self.position[0], self.position[1], image=self.img, tags=(f"{self.color}_city", "city"))
        return self.id

    def __repr__(self):
        return f"City:(color:{self.color}, index:{self.index}, position:{self.position}, id:{self.id})"


class Road(object):
    def __init__(self, color, index, position):
        self.color = color
        self.index = index
        self.position = position
        self.id = None

    def draw_road(self, canvas):
        self.id = canvas.create_line(placements_parts_builds_in_game[1][self.position[0] - 155][0],
                               placements_parts_builds_in_game[1][self.position[0] - 155][1],
                               placements_parts_builds_in_game[1][self.position[1] - 155][0],
                               placements_parts_builds_in_game[1][self.position[1] - 155][1], fill=colors[0], width=5,
                               activewidth=8, tags=("road", f"{self.color}_road"))
        return self.id

    def __repr__(self):
        return f"Road:(color:{self.color}, index:{self.index}, position:{self.position}, id:{self.id})"


class Boat(Road):
    def __init__(self, color, index, position, image1):
        super().__init__(color=color, index=index, position=position)
        print(image1)
        self.image = image1
        # self.image = self.image NOT TO DELETE

    def draw_boat(self, canvas):
        self.id = canvas.create_line(placements_parts_builds_in_game[1][self.position[0] - 155][0],
                                     placements_parts_builds_in_game[1][self.position[0] - 155][1],
                                     placements_parts_builds_in_game[1][self.position[1] - 155][0],
                                     placements_parts_builds_in_game[1][self.position[1] - 155][1], fill=colors[0], width=5,
                                     activewidth=8, tags=("road", f"{self.color}_road"))
        self.id = (self.id, canvas.create_image(placements_parts_builds_in_game[0][self.index][0], placements_parts_builds_in_game[0][self.index][1], tags=("boat", f"{self.color}_boat"), image=self.image))
        return self.id

    def __repr__(self):
        return f"Boat:(color:{self.color}, index:{self.index}, position:{self.position}, id:{self.id}, image:{self.image})"


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
    root.mainloop()
