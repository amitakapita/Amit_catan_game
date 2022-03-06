class Player(object):
    def __init__(self, id_game, color, conn, player_name):
        self.id_game = id_game
        self.color = color
        self.is_my_turn = False
        self.conn = conn
        self.player_name = player_name
        self.materials = {"grain": 0, "lumber": 0, "brick": 0, "wool": 0, "ore": 0, "development_card": 0}
        self.points = 0

    def increase_points(self, amount_increase_player=1):
        self.points += amount_increase_player

    def change_color(self, new_color_player):
        if self.color != new_color_player:
            self.color = new_color_player

    def increase_material(self, material, amount_inc):
        self.materials[material] += amount_inc

    def decrease_material(self, material, amount_dec):
        self.materials[material] -= amount_dec

    def change_turn(self, state: bool):
        self.is_my_turn = state

