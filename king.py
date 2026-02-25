from piece import Piece
from rule import Rule

rule = Rule()

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, "K", position, False)
    
    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col

        if start == end:
            return False

        if dy == 2 or dy == -2:
            castling_allowed, rook_col, rook_row, step, rook = self.castling(board, start, end)
            if castling_allowed:
                return True
            return False

        if 0 < dx ** 2 + dy ** 2 <= 2:
            if board[end_row][end_col] != "" and board[end_row][end_col].color == self.color:
                return False
            return True
        return False
    
    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        dx = end_row - start_row
        dy = end_col - start_col

        if dy == 2 or dy == -2:
            castling_allowed, rook_col, rook_row, step, rook = self.castling(board, start, end)
            if castling_allowed:
                board[end_row][end_col] = self
                board[start_row][start_col] = ""
                self.has_moved = True

                board[rook_row][rook_col] = ""
                if step == 1:
                    board[rook_row][end_col + 1] = rook
                else:
                    board[rook_row][end_col - 1] = rook
                rook.has_moved = True
        else:
            board[end_row][end_col] = self
            board[start_row][start_col] = ""
            self.has_moved = True
        
    def castling(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col
    
        if self.has_moved:
            return False

        if dy == 2:
            rook_col = 7
        else:
            rook_col = 0

        rook_row = start_row
        rook = board[rook_row][rook_col]

        if rook == "" or rook.name != "R" or rook.has_moved:
            return False
        
        step = 1 if dy == -2 else -1
        for col in range(start_col + step, end_col, step):
            if board[end_row][col] != "":
                return False

        return True, rook_col, rook_row, step, rook

    