import random
import threading
import socket

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

    def join_a_player(self, player_name):
        if self.count_players > self.maximum_players:
            self.players[player_name] = {"id": self.count_players, "materials": {"grain": 0, "lumber": 0, "brick": 0, "wool": 0, "ore": 0, "development_card": 0}, "points": 0, "color": colors[self.count_players - 1], "is_my_turn": False}
            self.count_players += 1

    def player_exits_the_room(self, player_name):
        self.count_players -= 1
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
            self.join_a_player(self.leader_name)

            while True:
                print(f"Players: {self.count_players} out of {self.maximum_players}")
                client_socket, client_address = server_socket.accept()
                print(f"A new client has conencted! {client_address}")
                self.join_a_player()
