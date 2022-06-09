import random
import threading
import socket
import protocol_library
import sqlite3 as sql
from protocol_library import client_commands, server_game_rooms_commands
import json
from player_game import Player
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


class GameRoom(object):
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
        self.ids_placements = []
        self.settlements = []  # (index, settlement)
        self.cities = []  # (index, city)
        self.roads = []  # (index, boat)
        self.boats = []  # (index, road)
        self.results_cubes = None
        self.players_recourses = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        self.dict_colors_indexes = {"bricks": 4, "iron": 3, "wheat": 2, "lumber": 1, "field": 0}
        self.dict_colors_players_indexes = {"firebrick4": 0, "SteelBlue4": 1, "chartreuse4": 2, "#DBB600": 3}
        self.is_first_round = True
        self.turns_of = None
        self.server_socket1 = None
        self.top_roads_and_boats = 5  # None 0
        self.current_index_turns_of = 0

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
            self.server_socket1 = server_socket  # a pointer

            while self.server_open:
                if self.count_players == 0:
                    print("Listening for new clients...")
                print("meow meow hav hav 1 1 hav meow")
                client_socket, client_address = server_socket.accept()
                print(f"A new client has conencted! {client_address}")
                if self.current == "waiting":
                    self.count_players += 1
                print(f"Players: {self.count_players} out of {self.maximum_players}")
                """if self.count_players == 1:
                    self.join_a_player(self.leader_name)
                else:
                    self.join_a_player()"""
                print("hi meow hav")
                self.handle_client(client_socket)
            server_socket.close()

        except socket.error as e:
            print(e)

    def handle_player_conn(self, conn):
        try:
            con = sql.connect("Data_Bases/accounts_database.db")
            while True:
                request = conn.recv(1024).decode()
                if request is None or request == "":
                    raise ConnectionError
                print(f"\n[Client {conn.getpeername()}] {request}")
                status = self.handle_client_cmd(conn, request, con)
                if status is not None and status == "CLOSING SERVER":
                    raise BaseException
        except ConnectionError:
            print(f"There was an error with the client {conn.getpeername()}, so the server closed the socket with him")
            self.player_exits_the_room(conn)
            self.send_information_of_players(is_leave=True)
            if self.current == "playing":
                if not self.count_players == 1:
                    if 2 <= self.count_players <= 3 and self.current_index_turns_of == 0:
                        self.turns_of = self.players[self.current_index_turns_of % self.count_players]
                        self.current_index_turns_of = self.current_index_turns_of % self.count_players
                    elif 2 <= self.count_players <= 3 and self.current_index_turns_of >= 1:
                        self.turns_of = self.players[(self.current_index_turns_of + 1) % self.count_players]
                        self.current_index_turns_of = (self.current_index_turns_of + 1) % self.count_players
                    print(f"Current player: {self.turns_of.player_name}, current index: {self.current_index_turns_of}")
                    self.send_who_turns_of()
                else:
                    msg_send = protocol_library.build_message(server_game_rooms_commands["close_lobby_ok_cmd"],
                                                              "game server closed, switched back to the main server")
                    print(f"[Server] -> [Client {self.players[0].conn.getpeername()}] {msg_send}")
                    self.players[0].conn.sendall(msg_send.encode())
                    self.players[0].conn.close()
                    self.server_open = False  # closing server
                    self.server_socket1.close()  # closing server
        except ConnectionRefusedError or ConnectionResetError or ConnectionAbortedError:
            pass
        except OSError:
            print(f"There was an error with the last client, so the server closed the socket with him")
            self.player_exits_the_room(conn)
            self.send_information_of_players(is_leave=True)
            if len(self.players) == 0:
                self.server_open = False
                self.server_socket1.close()  # #
                print("The server has closed")
        except BaseException as e:
            print("meow hav meow meow hav hav meow hav", e, traceback.format_exc())
            # self.server_socket1.close()  #
            conn.close()
            sys.exit(0)
        finally:
            if con:
                con.close()
                print(f"DB Connection has closed with [Client] {conn}")

    def handle_client(self, conn):
        client_handler = threading.Thread(target=self.handle_player_conn,
                                          args=(conn,))  # the comma is necessary
        client_handler.daemon = True
        client_handler.start()
        threads1.append(client_handler)

    def handle_client_cmd(self, conn, request, con):
        cmd, msg = protocol_library.disassemble_message(request)
        cmd_send, msg_send = "", ""
        if cmd == client_commands["join_my_player_cmd"]:
            if not self.is_full and self.current == "waiting" and msg not in [player.player_name for player in self.players]:
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
                if self.current == "playing":
                    message = protocol_library.build_message(server_game_rooms_commands["leave_player_ok_cmd"],
                                                             self.players_information())
                    for player in self.players:
                        print(f"[Server] -> [Client {player.conn.getpeername()}] {message}")
                        conn.sendall(message.encode())
                else:
                    message = protocol_library.build_message(server_game_rooms_commands["close_lobby_ok_cmd"],
                                                             "game server closed, switched back to the main server")
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
            # self.player_exits_the_room(conn)
            message = protocol_library.build_message(server_game_rooms_commands["leave_player_ok_cmd"],
                                                     self.players_information())
            if len(self.players) > 1:
                for player in self.players:
                    print(f"[Server] -> [Client {player.conn.getpeername()}] {message}")
                    conn.sendall(message.encode())
            elif self.count_players == 1:
                self.server_open = False
                self.players[0].conn.close()
            return
        elif cmd == client_commands["start_game_cmd"]:
            if self.count_players >= 2:
                print("meow meow")
                self.generate_map()
                self.start_game(self.tiles)
            return
        elif cmd == client_commands["buy_building_cmd"]:
            msg = msg.split("#")
            message = self.handle_buttons(msg[0], msg[1],
                                          self.is_first_round)  # index 0 - 266 (including them both), current button
            if not message[0]:
                cmd_send = server_game_rooms_commands["buy_building_failed_cmd"]
                conn.sendall(protocol_library.build_message(cmd_send, message[1]).encode())
                print(
                    f"[SERVER] -> [CLIENT {conn.getpeername()}] {protocol_library.build_message(cmd_send, message[1])}")
                return
            else:
                cmd_send = server_game_rooms_commands["buy_building_ok_cmd"]
                msg_send = f"{message[1]}*{self.is_first_round}*"
                for player in self.players:
                    if self.turns_of.player_name == player.player_name:
                        msg_send += f"{self.players_recourses[self.dict_colors_players_indexes[self.turns_of.color]]}*True"
                    else:
                        msg_send += f"{str(self.players_recourses[self.dict_colors_players_indexes[self.turns_of.color]][-1])}*False"
                    msg_send = msg_send + f"*{self.turns_of.sum_rounds_and_boats}*{self.turns_of.points}"
                    message1 = protocol_library.build_message(cmd_send, msg_send)
                    player.conn.sendall(message1.encode())
                    print(f"[SERVER] -> [CLIENT {player.conn.getpeername()}] {message1}")
                    msg_send = f"{message[1]}*{self.is_first_round}*"  # {self.players_recourses[self.dict_colors_players_indexes[self.turns_of.color]]}*
                return
        elif cmd == client_commands["pull_cubes_cmd"]:
            self.pull_cubes()
            return
        elif cmd == client_commands["finished_my_turn_cmd"]:
            if self.turns_of.points >= 12:
                # won
                msg_send = protocol_library.build_message(server_game_rooms_commands["Wined_cmd"],
                                                          f"{self.turns_of.player_name}*{self.turns_of.color}")
                self.send_for_all_players(msg_send)
                for player in self.players:  # quits the players from the game room
                    print(f"[Server] -> [Client {player.conn.getpeername()}] {msg_send}")
                    conn.sendall(msg_send.encode())
                    self.update_DB_player_win(player.player_name, player.color == self.turns_of.color, con)  #
                    self.player_exits_the_room(player.conn)
                    player.conn.close()
                self.server_open = False  # closing server
                self.server_socket1.close()  # closing server
                print("The server has closed")  # closing server
            elif self.is_first_round and self.players.index(self.turns_of) + 1 >= self.count_players:
                self.is_first_round = False
            if self.turns_of.player_name == self.players[(self.players.index(self.turns_of) + 1) % self.count_players].player_name:
                msg_send = protocol_library.build_message(server_game_rooms_commands["close_lobby_ok_cmd"],
                                                             "game server closed, switched back to the main server")
                for player in self.players:  # quits the players from the game room
                    print(f"[Server] -> [Client {player.conn.getpeername()}] {msg_send}")
                    conn.sendall(msg_send.encode())
                    player.conn.close()
                self.server_open = False  # closing server
                self.server_socket1.close()  # closing server
                return "CLOSING SERVER"
            self.turns_of = self.players[(self.players.index(self.turns_of) + 1) % self.count_players]
            self.current_index_turns_of = (self.players.index(self.turns_of) + 1) % self.count_players
            self.send_who_turns_of()
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
            list1 = json.dumps(
                list1 if list1 != [] else [(player_name.player_name, player_name.color) for player in self.players])
            return list1
        except Exception as e:
            print(e)

    def start_game(self, tiles):
        self.current = "playing"  # starting the game from the waiting room
        for value in self.players:
            conn = value.conn  # conn
            for i in range(0, 41, 5):  # 9 times in average the last one is 38 + 5 = 43 the last index in the tiles
                time.sleep(0.01)
                print(i, i + 5)
                conn.sendall(protocol_library.build_message(server_game_rooms_commands["start_game_ok"],
                                                            f"{json.dumps(tiles[i:i + 5], cls=BitPortGameEncoder)}").encode())  # #{len(json.dumps(ports, cls=BitPortGameEncoder))} len()
                message = protocol_library.build_message(server_game_rooms_commands["start_game_ok"],
                                                         f"{json.dumps(tiles[i:i + 5], cls=BitPortGameEncoder)}")  # #{len(json.dumps(ports, cls=BitPortGameEncoder))} len()
                print(f"[Server] -> [Client {conn.getpeername()}] {message}")
            message = protocol_library.build_message(server_game_rooms_commands["turn_who_cmd"],
                                                     f"firebrick4*{self.players[0].player_name}*{self.is_first_round}")  # at the beggining the turn is in red's
            conn.sendall(message.encode())
            print(f"\n[Server] -> [Client {conn.getpeername()}] {message}")
            self.turns_of = self.players[0]

    def send_information_of_players(self, is_leave=False):
        if not is_leave:
            cmd_send = server_game_rooms_commands["join_player_ok_cmd"]
        else:
            cmd_send = server_game_rooms_commands["leave_player_ok_cmd"]
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
                                           tile1.number != 6 and tile1.number != 8 and tile1.terrain_kind != "gold_mine"
                                           and tile1.terrain_kind != "sea"])
                print(gold_mine_tile, temp_tile)
                self.tiles[gold_mine_tile.index].number, self.tiles[
                    temp_tile.index].number = temp_tile.number, gold_mine_tile.number
                # self.tiles[gold_mine_tile.index].change_photo_number()
                # self.tiles[temp_tile.index].change_photo_number()
                print(gold_mine_tile, temp_tile)
        if gold_mine_tiles[0].index in forbidden_placements[gold_mine_tiles[1].index]:  # near to the other gold mine
            tile_xchange = random.choice(
                self.tiles[:gold_mine_tiles[0].index] + self.tiles[gold_mine_tiles[1].index + 1:] + self.tiles[
                                                                                                    gold_mine_tiles[
                                                                                                        0].index + 1:
                                                                                                    gold_mine_tiles[
                                                                                                        1].index])
            # tile_xchange points to the same id in the memory as the selected tile
            while tile_xchange.index in forbidden_placements[gold_mine_tiles[1].index]:
                tile_xchange = random.choice(
                    self.tiles[:gold_mine_tiles[0].index] + self.tiles[gold_mine_tiles[1].index + 1:] + self.tiles[
                                                                                                        gold_mine_tiles[
                                                                                                            0].index + 1:
                                                                                                        gold_mine_tiles[
                                                                                                            1].index])
                # tile_xchange points to the same id in the memory as the selected tile
            # swap placements and indexes
            self.tiles[gold_mine_tiles[0].index].placement, self.tiles[
                tile_xchange.index].placement = tile_xchange.placement, gold_mine_tiles[0].placement
            self.tiles[gold_mine_tiles[0].index].index, self.tiles[tile_xchange.index].index = tile_xchange.index, gold_mine_tiles[0].index
            self.tiles[gold_mine_tiles[0].index], self.tiles[tile_xchange.index] = self.tiles[tile_xchange.index], self.tiles[gold_mine_tiles[0].index]

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
        for placement in near_road_boat_numbers_indexes[
            index_road]:  # a road is near the placement that is of the player or a boat is near the placement that is of the player
            for index_road1 in self.roads:
                if index_road1[0] == placement and index_road1[1].color == color:
                    return True
            for index_boat1 in self.boats:
                if index_boat1[0] == placement and index_boat1[1].color == color:
                    return True
        return False

    def checking_settlement(self, position, color, first_turn):
        for index_settlement in self.settlements:  # if there is already a settlement or a city in this index
            if index_settlement[0] == position:
                return False
        for index_city in self.cities:  # about the city if there is already a settlement or a city in this index
            if index_city[0] == position:
                return False
        if not first_turn:
            # check in the not first round if the player builds a settlement near a road or a boat, else it is illegal
            finished_check = False
            for index in roads_and_boats_near_settlement_or_city_indexes[position - 155]:
                if finished_check:
                    break
                for road in self.roads:
                    print(index == road[1].index, index, road[1].index, road)
                    if index == road[0] and road[1].color == color:
                        finished_check = True
                        break
                for boat in self.boats:
                    print(boat[1].index == index and boat[1].color == color, index, boat[1].index, color, boat[1].color)
                    if boat[1].index == index and boat[1].color == color:
                        finished_check = True
                        break
            if not finished_check:
                return False
        counter_sea_tiles_and_Nones = 0
        for index3, tile in enumerate([index for index in what_part_is_on_what_tile_hex[1][
            position - 155]]):  # if there is not only seas or Nones
            if tile is None or self.tiles[tile].terrain_kind == "sea":
                counter_sea_tiles_and_Nones += 1
                print(counter_sea_tiles_and_Nones, tile)
                continue
            tile = self.tiles[tile]
            print(
                f"\n{tile}\n{places_in_each_placements_for_the_hexes[1][position - 155][index3]}\n{tile.check_validation_parts_in_the_game(places_in_each_placements_for_the_hexes[1][position - 155][index3])}\n{counter_sea_tiles_and_Nones}")
            if not tile.check_validation_parts_in_the_game(places_in_each_placements_for_the_hexes[1][position - 155][
                                                               index3]):  # fi it's valid from the fact that it can be only after 2 roads and that
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
        for placement in near_road_boat_numbers_indexes[
            index_boat]:  # a road is near the placement that is of the player or a boat is near the placement that is of the player
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
                    if (self.checking_city_or_settlement_is_near_the_road(position1,
                                                                          self.turns_of.color) or self.checking_roads_or_boats_is_near_the_road(
                        position1, self.turns_of.color)) and self.check_parts_in_game_recources("road", first_round,
                                                                                                self.turns_of.color):
                        road = Road(index=position1, color=self.turns_of.color,
                                    position=indexes_roads_xyx1y1_positions[position1])
                        # road.draw_road(self.canvas)
                        self.roads.append((position1, road))
                        for tile in what_part_is_on_what_tile_hex[0][position1]:
                            if tile is not None:
                                tile = self.tiles[tile]
                                tile.add_building(road, places_in_each_placements_for_the_hexes[0][position1],
                                                  is_settlement_or_city=False)
                                print(tile)
                        msg = json.dumps(road, cls=BitPortGameEncoder)
                        # self.canvas.tag_lower("road", "settlement")  # that for the assuming that roads are built after placing settlements and over and more
                        self.turns_of.sum_rounds_and_boats += 1
                        self.the_highest_amount_of_roads_and_boats(self.turns_of.sum_rounds_and_boats)
                elif current_button == "boat":
                    if (self.checking_boats_is_near_a_settlement_or_city(position1,
                                                                        self.turns_of.color) or self.checking_boats_is_near_the_road_or_a_boat(
                        position1, self.turns_of.color)) and self.check_parts_in_game_recources("boat", first_round,
                                                                                               self.turns_of.color):
                        boat = Boat(index=position1, color=self.turns_of.color,
                                    position=(indexes_roads_xyx1y1_positions[position1]), image1=None)
                        # boat.draw_boat(self.canvas)
                        self.boats.append((position1, boat))
                        for tile in what_part_is_on_what_tile_hex[0][position1]:
                            if tile is not None:
                                tile = self.tiles[tile]
                                tile.add_building(boat, places_in_each_placements_for_the_hexes[0][position1],
                                                  is_settlement_or_city=False)
                                print(tile)
                        # self.canvas.tag_lower("boat", "settlement")  # that for the assuming that roads are built after placing settlements and over and more
                        # and in order to see the boat's image
                        # self.canvas.tag_lower("road", "boat")
                        msg = json.dumps(boat, cls=BitPortGameEncoder)
                        self.turns_of.sum_rounds_and_boats += 1
                        self.the_highest_amount_of_roads_and_boats(self.turns_of.sum_rounds_and_boats)
                        for player in self.players:
                            print(player.sum_rounds_and_boats)
            elif 267 > position1 > 154:
                if current_button == "city":
                    for index, settlement in self.settlements:
                        if index == position1 and settlement.color == self.turns_of.color and self.check_parts_in_game_recources(
                                "city", first_round, self.turns_of.color):
                            # self.canvas.delete(settlement.id)
                            self.settlements.remove((index, settlement))
                            city1 = City(color=self.turns_of.color, index=position1,
                                         position=(placements_parts_builds_in_game[0] + placements_parts_builds_in_game[1])[int(position1)],
                                         img=None)
                            print(city1)  # not to delete
                            # city1.draw_city(self.canvas)
                            print(city1)  # not to delete
                            self.cities.append((position1, city1))
                            for index2, tile_index in enumerate(
                                    [index for index in what_part_is_on_what_tile_hex[1][position1 - 155]]):
                                if tile_index is not None:
                                    tile_index1 = self.tiles[tile_index]
                                    tile_index1.delete_building(
                                        places_in_each_placements_for_the_hexes[1][position1 - 155][index2])
                                    tile_index1.add_building(city1, places_in_each_placements_for_the_hexes[1][
                                        position1 - 155][index2], is_settlement_or_city=True)
                                    print(index2, tile_index1, tile_index)
                            print(self.settlements)
                            print(self.cities)
                            msg = json.dumps(city1, cls=BitPortGameEncoder)
                            self.turns_of.points += 1
                            break
                elif current_button == "settlement":
                    if self.checking_settlement(position1, self.turns_of.color, first_round) and self.check_parts_in_game_recources(
                            "settlement", first_round, self.turns_of.color):
                        settlement1 = Settlement(color=self.turns_of.color, index=int(position1),
                                                 position=(placements_parts_builds_in_game[0] + placements_parts_builds_in_game[1])[int(position1)],
                                                 img=None)
                        print(settlement1)
                        # settlement1.draw_settlement(self.canvas)
                        index2 = 0
                        for index1 in [index for index in what_part_is_on_what_tile_hex[1][position1 - 155]]:
                            if index1 is not None:
                                tile = self.tiles[index1]
                                print(tile, index1)
                                tile.add_building(building=settlement1,
                                                  index1=places_in_each_placements_for_the_hexes[1][position1 - 155][
                                                      index2], is_settlement_or_city=True)
                            index2 += 1
                        self.settlements.append((position1, settlement1))
                        msg = json.dumps(settlement1, cls=BitPortGameEncoder)
                        self.turns_of.points += 1
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
            msg_to_send = protocol_library.build_message(cmd=server_game_rooms_commands["pulled_cubes_cmd"],
                                                         msg=f"{json.dumps(self.results_cubes)}#"
                                                             f"{json.dumps(self.players_recourses[self.dict_colors_players_indexes[player.color]])}#"
                                                             f"{self.turns_of.player_name}#"
                                                             f"{[self.players_recourses[i][-1] for i in range(self.count_players)]}")
            player.conn.sendall(msg_to_send.encode())
            print(f"[Server] -> [Client {player.conn.getpeername()}] {msg_to_send}")

    def what_tile_is_on(self):
        if self.results_cubes[2] == 7:
            for player_recourses_list in self.players_recourses:
                sum1 = sum(player_recourses_list[:-1])  # the last one is a sum
                if sum1 > 10:
                    sum1 = sum1 // 2
                    print(sum1)
                    for _ in range(sum1):
                        recourse_index = random.choice(
                            [index for index, free_index in enumerate(player_recourses_list[:-1]) if free_index != 0])
                        player_recourses_list[recourse_index] -= 1
                    player_recourses_list[-1] -= sum1
        for tile in self.tiles:
            if tile.number == self.results_cubes[2]:
                for part_in_game in tile.parts_in_game:
                    print(part_in_game[1])
                    if tile.terrain_kind == "gold_mine":
                        if Type[type(part_in_game[1])] == Type[Settlement]:
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][
                                random.randint(0, 4)] += 1
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][-1] += 1
                        elif Type[type(part_in_game[1])] == Type[City]:
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][
                                random.randint(0, 4)] += 1  # 2
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][
                                random.randint(0, 4)] += 1  # 2 random resources at all
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][-1] += 2
                    else:
                        if Type[type(part_in_game[1])] == Type[Settlement]:
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][
                                self.dict_colors_indexes[tile.terrain_kind]] += 1
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][-1] += 1
                        elif Type[type(part_in_game[1])] == Type[City]:
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][
                                self.dict_colors_indexes[tile.terrain_kind]] += 2
                            self.players_recourses[self.dict_colors_players_indexes[part_in_game[1].color]][-1] += 2

    def check_parts_in_game_recources(self, building_part, first_round, color):
        if first_round and (building_part == "settlement" or building_part == "road" or building_part == "boat"):
            return True
        elif first_round:
            return False
        if building_part == "settlement":
            if self.players_recourses[self.dict_colors_players_indexes[color]][
                self.dict_colors_indexes["wheat"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][
                        self.dict_colors_indexes["lumber"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][
                        self.dict_colors_indexes["bricks"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][
                        self.dict_colors_indexes["field"]] > 0:
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["wheat"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["bricks"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["field"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][-1] -= 4
                return True
        elif building_part == "road":
            if self.players_recourses[self.dict_colors_players_indexes[color]][
                self.dict_colors_indexes["lumber"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][
                        self.dict_colors_indexes["bricks"]] > 0:
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["bricks"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][-1] -= 2
                return True
        elif building_part == "boat":
            if self.players_recourses[self.dict_colors_players_indexes[color]][
                self.dict_colors_indexes["lumber"]] > 0 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][
                        self.dict_colors_indexes["field"]] > 0:
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["lumber"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["field"]] -= 1
                self.players_recourses[self.dict_colors_players_indexes[color]][-1] -= 2
                print("meow")
                return True
        elif building_part == "city":
            if self.players_recourses[self.dict_colors_players_indexes[color]][
                self.dict_colors_indexes["iron"]] >= 3 and \
                    self.players_recourses[self.dict_colors_players_indexes[color]][
                        self.dict_colors_indexes["wheat"]] >= 2:
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["iron"]] -= 3
                self.players_recourses[self.dict_colors_players_indexes[color]][self.dict_colors_indexes["wheat"]] -= 2
                self.players_recourses[self.dict_colors_players_indexes[color]][-1] -= 5
                return True
        return False

    def send_who_turns_of(self):
        message = protocol_library.build_message(server_game_rooms_commands["turn_who_cmd"],
                                                 f"{self.turns_of.color}*{self.turns_of.player_name}*{self.is_first_round}")
        for player in self.players:
            player.conn.sendall(message.encode())
            print(f"[SERVER] -> [CLIENT {player.conn.getpeername()}] {message}")

    def send_for_all_players(self, message):
        for player in self.players:
            player.conn.sendall(message.encode())
            print(f"[SERVER] -> [CLIENT {player.conn.getpeername()}] {message}")

    def the_highest_amount_of_roads_and_boats(self, number_amount):
        print(type(self.top_roads_and_boats), type(self.top_roads_and_boats) == int,
              type(self.top_roads_and_boats) == Player)
        if type(self.top_roads_and_boats) == int:  # type(int)
            if number_amount > self.top_roads_and_boats:
                # if not self.players[index].color == self.top_roads_and_boats.color:
                self.turns_of.points += 2
                # self.
                # self.players_recourses[index][-1] += 2
                # self.players_recourses[self.players.index(self.top_roads_and_boats)][-1] -= 2
                # else:
                self.top_roads_and_boats = [number_amount,
                                            self.players.index(self.turns_of)]  # (number_amount, index_player)
        elif type(self.top_roads_and_boats) == list and number_amount > self.top_roads_and_boats[0]:  # and number_amount > 5
            if not self.turns_of.color == self.players[self.top_roads_and_boats[1]].color:
                self.turns_of.points += 2
                self.players[self.top_roads_and_boats[1]].points -= 2
                self.send_for_all_players(protocol_library.build_message(
                    server_game_rooms_commands["update_points_cmd"],
                    f"{self.players[self.top_roads_and_boats[1]].points}*{self.players[self.top_roads_and_boats[1]].color}"
                ))
                self.top_roads_and_boats = [number_amount, self.players.index(self.turns_of)]
            else:
                self.top_roads_and_boats[0] = number_amount

    def update_DB_player_win(self, player_name, is_winner, con):
        cur = con.cursor()
        cur.execute("SELECT Played_games, Wined_games FROM accounts WHERE Username = ?", (player_name,))
        points = cur.fetchall()
        print(int(str(points[0][0])) + 1, int(str(points[0][1])) + 1)
        cur.execute("""UPDATE accounts SET Played_games = ? WHERE Username = ?""", (int(str(points[0][0])) + 1, player_name))
        if is_winner:
            cur.execute("""UPDATE accounts SET Wined_games = ? WHERE Username = ?""", (int(str(points[0][1])) + 1, player_name))
        con.commit()
        cur.close()



if __name__ == "__main__":
    try:
        ip = "0.0.0.0"
        # print("meow hav hav meow meow hav meow hav")
        leader_name, maximum_players, session_id, port = sys.argv[1:]
        print(leader_name, maximum_players, port, ip, session_id)
        print(sys.argv[:])
        time.sleep(0.5)
        game_server1 = GameRoom(leader_name=leader_name, ip1=ip, port1=int(port), maximum_players=maximum_players,
                                session_id=session_id)
        game_server1.start()
        print("meow meow hav hav 123")
    except Exception as e:
        print(e, "meow hav")
        time.sleep(5)
