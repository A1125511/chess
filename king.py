from piece import Piece

class King(Piece):
    def __init__(self, color):
        super().__init__(color, "K")
        self.first_move = True
    
    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col

        if 0 < dx ** 2 + dy ** 2 <= 2:
            if board[end_row][end_col] != "" and board[end_row][end_col].color == self.color:
                return False
            
            board[end_row][end_col] = self
            board[start_row][start_col] = ""
            self.first_move = False
            return True

        return False