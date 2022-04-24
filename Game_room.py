import random
import threading
import socket
import protocol_library
import sqlite3 as sql
from protocol_library import client_commands, server_game_rooms_commands
import json
from player_game import  Player
import sys
import time
import subprocess
import signal
import os
import traceback
from some_from_hex_tile import *
import time

colors = ["firebrick4", "SteelBlue4", "chartreuse4", "#DBB600"]
subprocess1 = ""
threads1 = []


class GameRoom (object):
    def __init__(self, leader_name, maximum_players, ip1, port1, session_id):
        self.session_id = session_id
        self.leader_name = leader_name
        self.players = []
        self.maximum_players = int(maximum_players)
        self.current = "waiting"  # "creating"
        self.count_players = 0
        self.ip = ip1
        self.port = port1
        self.is_full = False
        self.server_open = True
        self.tiles = []
        self.ports = []
        self.ids_placements = []
        self.settlements = []  # (index, settlement)
        self.cities = []  # (index, city)
        self.roads = []
        self.boats = []
        self.results_cubes = None
        self.players_recourses = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.dict_colors_indexes = {"bricks": 4, "iron": 3, "wheat": 2, "lumber": 1, "field": 0}
        self.dict_colors_players_indexes = {"firebrick4": 0, "SteelBlue4": 1, "chartreuse4": 2, "#DBB600": 3}
        self.is_first_round = True

    def join_a_player(self, player_name, conn):
        if self.count_players <= self.maximum_players:
            player1 = Player(self.session_id, colors[self.count_players - 1], conn, player_name)
            self.players.append(player1)
        print(self.players)

    def player_exits_the_room(self, conn):
        self.count_players -= 1
        if self.current == "waiting" and self.is_full:
            self.is_full = False
        for index, player in enumerate(self.players):
            if player.conn == conn:
                del self.players[index]
                break

    """def create_lobby(self):
        # self.players.append({self.leader_name})
        self.current = "waiting"""""

    def check_who_is_on(self):
        # if the cubes got 5, so it searches in the tiles that has 5 which player has a settlement or a city on it, then gives the source to him.
        pass

    def start(self):
        try:
            print(f"The server starts in ip: {self.ip}, and port: {self.port}, session_id is: {self.session_id}")
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("meow hi hav")
            server_socket.bind((self.ip, self.port))
            server_socket.listen()

            while self.server_open:
                if self.count_players == 0:
                    print("Listening for new clients...")
                print("meow meow hav hav 1 1 hav meow")
                client_socket, client_address = server_socket.accept()
                print(f"A new client has conencted! {client_address}")
                print(f"Players: {self.count_players} out of {self.maximum_players}")
                """if self.count_players == 1:
                    self.join_a_player(self.leader_name)
                else:
                    self.join_a_player()"""
                self.count_players += 1
                print("hi meow hav")
                self.handle_client(client_socket)

        except socket.error as e:
            print(e)

    def handle_player_conn(self, conn):
        try:
            while True:
                request = conn.recv(1024).decode()
                if request is None or request == "":
                    raise ConnectionError
                print(f"\n[Client {conn.getpeername()}] {request}")
                status = self.handle_client_cmd(conn, request)
                if status is not None and status == "CLOSING SERVER":
                    raise BaseException
        except ConnectionError or OSError:
            print(f"There was an error with the client {conn.getpeername()}, so the server closed the socket with him")
            self.player_exits_the_room(conn)
            self.send_information_of_players()
        except BaseException as e:
            print("meow hav meow meow hav hav meow hav", e, traceback.format_exc())
            sys.exit(0)
            conn.close()
        except ConnectionRefusedError or ConnectionResetError or ConnectionAbortedError:
            pass

    def handle_client(self, conn):
        client_handler = threading.Thread(target=self.handle_player_conn,
                                          args=(conn,))  # the comma is necessary
        client_handler.daemon = True
        client_handler.start()
        threads1.append(client_handler)

    def handle_client_cmd(self, conn, request):
        con = sql.connect("Data_Bases/accounts_database.db")
        cmd, msg = protocol_library.disassemble_message(request)
        cmd_send, msg_send = "", ""
        if cmd == client_commands["join_my_player_cmd"]:
            if not self.is_full and self.current == "waiting":
                print("meow hav meow 2 1 hav")
                self.join_a_player(msg, conn)
                self.send_information_of_players()
                return
            else:  # just in case
                cmd_send = server_game_rooms_commands["join_player_failed_cmd"]
        elif cmd == client_commands["get_players_information_cmd"]:
            cmd_send, msg_send = self.players_information()
        elif cmd == client_commands["close_lobby_cmd"]:
            print(self.players)
            if self.players[0].conn == conn:
                message = protocol_library.build_message(server_game_rooms_commands["close_lobby_ok_cmd"], "game server closed, switched back to the main server")
                for player in self.players:
                    print(f"[Server] -> [Client {player.conn.getpeername()}] {message}")
                    conn.sendall(message.encode())
                    self.player_exits_the_room(player.conn)
                    player.conn.close()

                print("CLOSING SERVER")
                self.server_open = False
                # sys.exit(1)
                return "CLOSING SERVER"
        elif cmd == client_commands["leave_my_player_cmd"]:
            self.player_exits_the_room(conn)
            message = protocol_library.build_message(server_game_rooms_commands["leave_player_ok_cmd"], self.players_information())
            for player in self.players:
                print(f"[Server] -> [Client {player.conn.getpeername()}] {message}")
                conn.sendall(message.encode())
            return
        elif cmd == client_commands["start_game_cmd"]:
            print("meow meow")
            self.generate_map()
            self.start_game(self.tiles, self.ports)
            return
        elif cmd == client_commands["buy_building_cmd"]:
            msg = msg.split("#")
            message = self.handle_buttons(msg[0], msg[1], self.is_first_round)  # index 0 - 266 (including them both), current button
            if not message[0]:
                cmd_send = server_game_rooms_commands["buy_building_failed_cmd"]
            else:
                cmd_send = server_game_rooms_commands["buy_building_ok_cmd"]
        elif cmd == client_commands["pull_cubes_cmd"]:
            self.pull_cubes()
            return
        message = protocol_library.build_message(cmd_send, msg_send)
        print(f"[Server] -> [Client {conn.getpeername()}] {message}")
        conn.sendall(message.encode())

    def players_information(self):
        try:
            list1 = []
            player_name: Player
            for index, player_name in enumerate(self.players):
                if player_name.get_color() != colors[index] and self.current == "waiting":
                    player_name.change_color(colors[index])
                    list1.append((player_name.player_name, player_name.color))
                elif self.current != "waiting" or player_name.get_color() == colors[index]:
                    list1.append((player_name.player_name, player_name.color))
            list1 = json.dumps(list1 if list1 != [] else [(player_name.player_name, player_name.color) for player in self.players])
            return list1
        except Exception as e:
            print(e)

    def start_game(self, tiles, ports):
        self.current = "playing"  # starting the game from the waiting room
        for value in self.players:
            conn = value.conn  # conn
            for i in range(0, 41, 5):  # 9 times in average the last one is 38 + 5 = 43 the last index in the tiles
                time.sleep(0.1)
                print(i, i + 5)
                conn.sendall(protocol_library.build_message(server_game_rooms_commands["start_game_ok"], f"{json.dumps(tiles[i:i + 5], cls=BitPortGameEncoder)}").encode())  # #{len(json.dumps(ports, cls=BitPortGameEncoder))} len()
                message = protocol_library.build_message(server_game_rooms_commands["start_game_ok"], f"{json.dumps(tiles[i:i + 5], cls=BitPortGameEncoder)}")  # #{len(json.dumps(ports, cls=BitPortGameEncoder))} len()
                print(f"[Server] -> [Client {conn.getpeername()}] {message}")

    def send_information_of_players(self):
        cmd_send = server_game_rooms_commands["join_player_ok_cmd"]
        msg_send = self.players_information()
        message = protocol_library.build_message(cmd_send, msg_send)
        for player in self.players:
            conn = player.conn
            print(f"[Server] -> [Client {conn.getpeername()}] {message}")
            conn.sendall(message.encode())

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
            temp_tile1 = HexTile1(temp_number, place, temp_tile, index)
            # temp_tile1 = [temp_number, place, temp_tile, index, False]
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
            # port1 = PortGame(placement_for_the_port, kind_of_the_port, placement1,
            #                  ports_games_degrees[placement_for_the_port], tile_temp)
            port1 = [placement_for_the_port, kind_of_the_port, placement1, ports_games_degrees[placement_for_the_port], tile_temp]
            # port1 = BitPortGame(placement_for_the_port, kind_of_the_port, placement1, ports_games_degrees[placement_for_the_port], tile_temp)
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
                # self.tiles[gold_mine_tile.index].change_photo_number()
                # self.tiles[temp_tile.index].change_photo_number()
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

    def handle_buttons(self, position, current_button, first_round):
        position1 = position
        msg = None
        if position1 != "":
            for element in position1:
                if element not in "1234567890":
                    return False, "an index is in numbers"
            position1 = int(position1)
            if 0 <= position1 <= 154:
                if current_button == "road":
                    # if there is not there any road, and there is a the player's settlement or city near, or there is a road of the player near
                    if (self.checking_city_or_settlement_is_near_the_road(position1, "red") or self.checking_roads_or_boats_is_near_the_road(position1, "red")) and self.check_parts_in_game_recources("road", first_round, "red"):
                        road = Road(index=position1, color="red", position=indexes_roads_xyx1y1_positions[position1])
                        # road.draw_road(self.canvas)
                        self.roads.append((position1, road))
                        for tile in what_part_is_on_what_tile_hex[0][position1]:
                            if tile is not None:
                                tile = self.tiles[tile]
                                tile.add_building(road, places_in_each_placements_for_the_hexes[0][position1], is_settlement_or_city=False)
                                print(tile)
                        msg = json.dumps(road)
                        # self.canvas.tag_lower("road", "settlement")  # that for the assuming that roads are built after placing settlements and over and more
                elif current_button == "boat":
                    if self.checking_boats_is_near_a_settlement_or_city(position1, "red") or self.checking_boats_is_near_the_road_or_a_boat(position1, "red") and self.check_parts_in_game_recources("boat", first_round, "red"):
                        boat = Boat(index=position1, color="red", position=(indexes_roads_xyx1y1_positions[position1]), image1=self.image_boat_1)
                        # boat.draw_boat(self.canvas)
                        self.boats.append((position1, boat))
                        for tile in what_part_is_on_what_tile_hex[0][position1]:
                            if tile is not None:
                                tile = self.tiles[tile]
                                tile.add_building(boat, places_in_each_placements_for_the_hexes[0][position1], is_settlement_or_city=False)
                                print(tile)
                        # self.canvas.tag_lower("boat", "settlement")  # that for the assuming that roads are built after placing settlements and over and more
                        # and in order to see the boat's image
                        # self.canvas.tag_lower("road", "boat")
                        msg = json.dumps(boat)
            elif 267 > position1 > 154:
                if current_button == "city":
                    for index, settlement in self.settlements:
                        if index == position1 and settlement.color == "red" and self.check_parts_in_game_recources("city", first_round, "red"):
                            # self.canvas.delete(settlement.id)
                            self.settlements.remove((index, settlement))
                            city1 = City(color="red", index=position1, position=(placements_parts_builds_in_game[0] + placements_parts_builds_in_game[1])[int(position1)], img=self.image_city_red)
                            print(city1)  # not to delete
                            # city1.draw_city(self.canvas)
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
                            msg = json.dumps(city1)
                            break
                elif current_button == "settlement":
                    if self.checking_settlement(position1, "red") and self.check_parts_in_game_recources("settlement", first_round, "red"):
                        settlement1 = Settlement(color="red", index=int(position1), position=(placements_parts_builds_in_game[0] + placements_parts_builds_in_game[1])[int(position1)], img=self.image1)
                        print(settlement1)
                        # settlement1.draw_settlement(self.canvas)
                        index2 = 0
                        for index1 in [index for index in what_part_is_on_what_tile_hex[1][position1 - 155]]:
                            if index1 is not None:
                                tile = self.tiles[index1]
                                print(tile, index1)
                                tile.add_building(building=settlement1, index1=places_in_each_placements_for_the_hexes[1][position1 - 155][index2], is_settlement_or_city=True)
                            index2 += 1
                        self.settlements.append((position1, settlement1))
                        msg = json.dumps(settlement1)
        if msg is not None:
            return True, msg
        else:
            return False, "the system could not place your building, check if your request is valid."

    def pull_cubes(self):
        cube1, cube2 = random.randint(1, 6), random.randint(1, 6)
        sum_cubes = cube1 + cube2
        self.results_cubes = (cube1, cube2, sum_cubes)
        self.what_tile_is_on()
        for player in self.players:
            msg_to_send = protocol_library.build_message(cmd=server_game_rooms_commands["pulled_cubes_cmd"], msg=f"{json.dumps(self.results_cubes)}#{json.dumps(self.players_recourses[self.dict_colors_players_indexes[player.color]])}")
            player.conn.sendall(msg_to_send.encode())
            print(f"[Server] -> [Client {player.conn.getpeername()}] {msg_to_send}")

    def what_tile_is_on(self):
        if self.results_cubes[2] == 7:
            for player_recourses_list in self.players_recourses:
                sum1 = sum(player_recourses_list)
                if sum1 > 7:
                    sum1 = sum1 // 2
                    for _ in range(sum1):
                        recourse_index = random.choice([index for index, free_index in enumerate(player_recourses_list) if free_index != 0])
                        player_recourses_list[recourse_index] -= 1
        for tile in self.tiles:
            if tile.number == self.results_cubes[2]:
                for part_in_game in tile.parts_in_game:
                    print(part_in_game[1])
                    if tile.terrain_kind == "gold_mine":
                        if Type[type(part_in_game[1])] == Type[Settlement]:
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][random.randint(0, 4)] += 1
                        elif Type[type(part_in_game[1])] == Type[City]:
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][random.randint(0, 4)] += 2
                    else:
                        if Type[type(part_in_game[1])] == Type[Settlement]:
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][self.dict_colors_indexes[tile.terrain_kind]] += 1
                        elif Type[type(part_in_game[1])] == Type[City]:
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][self.dict_colors_indexes[tile.terrain_kind]] += 2

    def check_parts_in_game_recources(self, building_part, first_round, color):
        if first_round and (building_part == "settlement" or building_part == "road" or building_part == "boat"):
            return True
        elif first_round:
            return False
        if building_part == "settlement":
            if self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["wheat"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["bricks"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["field"]] > 0:
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["wheat"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["bricks"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["field"]] -= 1
                return True
        elif building_part == "road":
            if self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["bricks"]] > 0:
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["bricks"]] -= 1
                return True
        elif building_part == "boat":
            if self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] > 0 and \
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["field"]] > 0:
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["field"]] -= 1
                return True
        elif building_part == "city":
            if self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["iron"]] >= 3 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["wheat"]] >= 2:
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["iron"]] -= 3
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["wheat"]] -= 2
                return True
        return False



if __name__ == "__main__":
    try:
        ip = "0.0.0.0"
        # print("meow hav hav meow meow hav meow hav")
        leader_name, maximum_players, session_id, port = sys.argv[1:]
        print(leader_name, maximum_players, port, ip, session_id)
        print(sys.argv[:])
        time.sleep(0.5)
        game_server1 = GameRoom(leader_name=leader_name, ip1=ip, port1=int(port), maximum_players=maximum_players, session_id=session_id)
        game_server1.start()
        print("meow meow hav hav 123")
    except Exception as e:
        print(e, "meow hav")
        time.sleep(5)
