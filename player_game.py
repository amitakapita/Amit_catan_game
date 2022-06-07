class Player(object):
    def __init__(self, id_game, color, conn, player_name):
        self.id_game = id_game
        self.color = color
        self.is_my_turn = False
        self.conn = conn
        self.player_name = player_name
        self.points = 0
        self.sum_rounds_and_boats = 0

    def change_color(self, new_color_player):
        if self.color != new_color_player:
            self.color = new_color_player

    def get_color(self):
        return self.color

    def __repr__(self):
        return f"{self.id_game}, {self.color}, {self.is_my_turn}, {self.conn}, {self.player_name}, {self.points}"  # , {self.materials}
