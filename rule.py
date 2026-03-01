class Rule:
    def __init__(self):
        self.state = ["w", "b"]
        self.index = 0

    def player_turn(self, current_player):
        current_state = self.state[self.index]
        if current_player == current_state:
            return True
        else:
            return False

    def next_player(self):
        self.index = (self.index + 1) % 2