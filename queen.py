from piece import Piece
from game_state import GameState
from pawn import Pawn

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, "Q", position, False)
    
    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col

        if start == end:
            return False

        if start_row == end_row or start_col == end_col:
            
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
            
            if board[end_row][end_col] != "" and board[end_row][end_col].color == self.color:
                return False

            if not GameState.is_safe_move(board, self, start, end):
                return False
            return True

        if dx * dx == dy * dy:
            
            step_x = 1 if end_row > start_row else -1
            step_y = 1 if end_col > start_col else -1

            x, y = start_row + step_x, start_col + step_y
            while (x, y) != (end_row, end_col) and 0 <= x < len(board) and 0 <= y < len(board[0]):
                if board[x][y] != "":
                    return False
                x += step_x
                y += step_y
            
            if board[end_row][end_col] != "" and board[end_row][end_col].color == self.color:
                return False
            if not GameState.is_safe_move(board, self, start, end):
                return False
            return True
        
        return False

    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        board[end_row][end_col] = self
        board[start_row][start_col] = ""

        Pawn.set_current_en_passant(None, None, None)

        self.has_moved = True
    
    def get_attacked_squares(self, board, start):
        start_row, start_col = start
        attacked_squares = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = start_row + dx, start_col + dy
            while 0 <= x < 8 and 0 <= y < 8:
                attacked_squares.append((x, y))
                if board[x][y] != "":
                    break
                x += dx
                y += dy

        for dx in [-1, 1]:
            for dy in [-1, 1]:
                x, y = start_row + dx, start_col + dy
                while 0 <= x < 8 and 0 <= y < 8:
                    attacked_squares.append((x, y))
                    if board[x][y] != "":
                        break
                    x += dx
                    y += dy
        
        return attacked_squares
    