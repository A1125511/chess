from piece import Piece
from game_state import GameState
from pawn import Pawn

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, "N", position, False)

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col

        if start == end:
            return False

        if dx ** 2 + dy ** 2 == 5:

            # capture
            if board[end_row][end_col] != "" and board[end_row][end_col].color ==self.color:
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
        self.has_moved = True

        Pawn.set_current_en_passant(None, None, None)

    def get_attacked_squares(self, board, start):
        start_row, start_col = start
        attacked_squares = []
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                if dx ** 2 + dy ** 2 == 5:
                    x, y = start_row + dx, start_col + dy
                    if 0 <= x < 8 and 0 <= y < 8:
                        attacked_squares.append((x, y))        
        return attacked_squares
    