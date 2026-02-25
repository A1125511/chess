# piece.py

class Piece:
    def __init__(self, color, name, initial_position=None, has_moved=False):
        self.color = color
        self.name = name
        self.initial_position = initial_position
        self.has_moved = has_moved
        
    def is_valid_move(self, board, start, end):
        raise NotImplementedError
        