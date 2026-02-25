class GameState:
    def __init__(self):
        self.is_white_perspective = True
    
    def getCurrentPlayer(self):
        return self.is_white_perspective

