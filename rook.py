from piece import Piece
from rule import Rule

rule = Rule()

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, "R", position, False)

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        if start == end:
            return False
            
        # move
        if start_row == end_row or end_col == start_col:
            # check path
            if start_row == end_row:
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[end_row][col] != "":
                        return False
            elif start_col == end_col:
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][end_col] != "":
                        return False
            
            # capture
            if board[end_row][end_col] != "" and board[end_row][end_col].color == self.color:
                return False
            
            return True

        return False

    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        board[end_row][end_col] = self
        board[start_row][start_col] = ""
        self.has_moved = True