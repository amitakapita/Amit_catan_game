import random
import threading


class GameRoom (object):
    def __init__(self, leader_name, maximum_players):
        self.session_id = random.randint(10000, 100000)
        self.leader_name = leader_name
        self.players = [{self.leader_name}]  # a list of dictionaries
        self.maximum_players = maximum_players

    def create_lobby(self):
        # self.players.append({self.leader_name})