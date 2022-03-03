import random
import threading
import socket
import protocol_library
import sqlite3 as sql
from protocol_library import client_commands, server_game_rooms_commands

colors = ["red", "blue", "green", "yellow"]


class GameRoom (object):
    def __init__(self, leader_name, maximum_players, ip1, port1):
        self.session_id = random.randint(10000, 100000)
        self.leader_name = leader_name
        self.players: dict = {}  # a list of dictionaries [{self.leader_name}]
        self.maximum_players = maximum_players
        self.current = "creating"
        self.count_players = 1
        self.ip = ip1
        self.port = port1
        self.is_full = False

    def join_a_player(self, player_name):
        if self.count_players > self.maximum_players:
            self.players[player_name] = {"id_game": self.count_players, "materials": {"grain": 0, "lumber": 0, "brick": 0, "wool": 0, "ore": 0, "development_card": 0}, "points": 0, "color": colors[self.count_players - 1], "is_my_turn": False}

    def player_exits_the_room(self, player_name):
        self.count_players -= 1
        if self.current == "waiting" and self.is_full:
            self.is_full = False
        del self.players[player_name]

    def create_lobby(self):
        # self.players.append({self.leader_name})
        self.current = "waiting"

    def check_who_is_on(self):
        # if the cubes got 5 so it searches in the tiles that has 5 which player has a settlement or a city on it, then gives the source to him.

    def start(self):
        try:
            print(f"The server start in ip: {self.ip}, and port: {self.port}")
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))
            server_socket.listen()

            while True:
                if self.count_players < self.maximum_players and self.current == "waiting":
                    print(f"Players: {self.count_players} out of {self.maximum_players}")
                    client_socket, client_address = server_socket.accept()
                    print(f"A new client has conencted! {client_address}")
                    """if self.count_players == 1:
                        self.join_a_player(self.leader_name)
                    else:
                        self.join_a_player()"""
                    self.count_players += 1
                    self.handle_client(client_socket)

        except socket.error as e:
            print(e)

    def handle_player_conn(self, conn):
        try:
            while True:
                request = conn.recv(1024).decode()
                if request is None or request == "":
                    raise ConnectionError
                print(f"\n[Client] {request}")
                self.handle_client_cmd(conn, request)
        except ConnectionError:
            print(f"There was an error with the client {conn.getpeername()}, so the server closed the socket with him")
            self.count_players -= 1
            conn.close()

    def handle_client(self, conn):
        client_handler = threading.Thread(target=self.handle_player_conn,
                                          args=(conn,))  # the comma is necessary
        client_handler.start()

    def handle_client_cmd(self, conn, request):
        con = sql.connect("Data_Bases/accounts_database.db")
        cmd, msg = protocol_library.disassemble_message(request)
        cmd_send, msg_send = "", ""
        if cmd == client_commands["join_my_player_cmd"]:
            if not self.is_full:
                self.join_a_player(msg)
                cmd_send = server_game_rooms_commands["join_player_ok_cmd"]
            else:  # just in case
                cmd_send = server_game_rooms_commands["join_player_failed_cmd"]
        message = protocol_library.build_message(cmd_send, msg_send)
        print(f"[Server] -> [{conn.getpeername()}] {message}")
        conn.sendall(message.encode())