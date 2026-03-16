import board
from piece import Piece

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, "B", position, False)

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col

        if start == end:
            return False

        if dx * dx == dy * dy:
            step_x = 1 if end_row > start_row else -1
            step_y = 1 if end_col > start_col else -1

            x, y = start_row + step_x, start_col + step_y
            while (x, y) != (end_row, end_col) and 0 <= x < len(board) and 0 <= y < len(board[0]):
                # print("x, y =", x, y)
                # print("len(board) =", len(board))
                # print("len(board[0]) =", len(board[0]))

                if board[x][y] != "":
                    return False
                x += step_x
                y += step_y

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
