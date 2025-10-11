
class p:
    def __init__(self, color, types):
        self.color = color
        self.types = types

type_pieces = {"pawn", "rook", "knight", "king", "queen"}
type_pieces = ["pawn", "rook", "knight", "king", "queen"]

board = [[None for _ in range(8)] for _ in range(8)]
board = [("Rook", "black", (0, 0))]

for type_pieces in type_pieces:
    board.append(type_pieces)

print(board[1][1])
