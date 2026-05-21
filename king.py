from piece import Piece
from rule import Rule
from game_state import GameState
from pawn import Pawn

rule = Rule()

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, "K", position, False)
        self.castling_type = None
    
    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col

        if start == end:
            return False

        if dx == 0 and (dy == 2 or dy == -2):
            castling_allowed, rook_col, rook_row, step, rook = self.castling(board, start, end)
            
            if castling_allowed:
                attacker_color = "b" if self.color == "w" else "w"
                for c in range(start_col, end_col + step, step):
                    if GameState.is_square_attacked(board, (end_row, c), attacker_color):
                        return False
                return True
            return False

        if 0 < dx ** 2 + dy ** 2 <= 2:
            if board[end_row][end_col] != "" and board[end_row][end_col].color == self.color:
                return False
            if not GameState.is_safe_move(board, self, start, end):
                return False
            return True
        return False
    
    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        dx = end_row - start_row
        dy = end_col - start_col

        if dx == 0 and (dy == 2 or dy == -2):
            castling_allowed, rook_col, rook_row, step, rook = self.castling(board, start, end)
            if castling_allowed:
                board[end_row][end_col] = self
                board[start_row][start_col] = ""
                self.has_moved = True

                board[rook_row][rook_col] = ""
                if step == -1:
                    board[rook_row][end_col + 1] = rook
                else:
                    board[rook_row][end_col - 1] = rook
                rook.has_moved = True
        else:
            board[end_row][end_col] = self
            board[start_row][start_col] = ""
            self.has_moved = True

        Pawn.set_current_en_passant(None, None, None)
        
    def castling(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col
    
        if self.has_moved:
            return False, None, None, None, None

        if dy == 2:
            rook_col = 7
        else:
            rook_col = 0

        rook_row = start_row
        rook = board[rook_row][rook_col]

        if rook == "" or rook.name != "R" or rook.has_moved:
            return False, None, None, None, None
            
        step = -1 if dy == -2 else 1
        for col in range(start_col + step, rook_col, step):
            if board[end_row][col] != "":
                return False, None, None, None, None
        
        return True, rook_col, rook_row, step, rook

    def get_attacked_squares(self, board, start):
        start_row, start_col = start
        attacked_squares = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_row, new_col = start_row + dx, start_col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    attacked_squares.append((new_row, new_col))        
        return attacked_squares

