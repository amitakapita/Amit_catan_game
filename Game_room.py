import random
import threading

colors = ["red", "blue", "green", "yellow"]


class GameRoom (object):
    def __init__(self, leader_name, maximum_players):
        self.session_id = random.randint(10000, 100000)
        self.leader_name = leader_name
        self.players: dict = {}  # a list of dictionaries [{self.leader_name}]
        self.maximum_players = maximum_players
        self.current = "creating"
        self.count_players = 1

    def join_a_player(self, player_name):
        if self.count_players > self.maximum_players:
            self.players[player_name] = {"id": self.count_players, "materials": {"grain": 0, "lumber": 0, "brick": 0, "wool": 0, "ore": 0, "development_card": 0}, "points": 0, "color": colors[self.count_players], "is_my_turn": False}
            self.count_players += 1

    def player_exits_the_room(self, player_name):
        self.count_players -= 1
        del self.players[player_name]

    def create_lobby(self):
        # self.players.append({self.leader_name})
        self.current = "waiting"

    def check_who_is_on(self):
        # if the cubes got 5 so it searches in the tiles that has 5 which player has a settlement or a city on it, then gives the source to him.
