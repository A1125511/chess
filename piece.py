# piece.py

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        
    def is_valid_move(self, board, start, end):
        raise NotImplementedError
        