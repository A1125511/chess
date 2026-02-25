from queen import Queen
from bishop import Bishop 
from knight import Knight
from rook import Rook

class Promotion_menu:
    def __init__(self):
        pass

    def show(color, key_name):
        match key_name:
            case "q":
                return Queen(color,position=None)
            case "b":
                return Bishop(color,position=None)
            case "n":
                return Knight(color,position=None)
            case "r":
                return Rook(color, position=None)
            case _:
                return None