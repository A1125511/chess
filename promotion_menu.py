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
                return Queen(color)
            case "b":
                return Bishop(color)
            case "n":
                return Knight(color)
            case "r":
                return Rook(color)
            case _:
                return None