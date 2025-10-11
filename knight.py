from piece import Piece

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "N")

    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col

        if dx ** 2 + dy ** 2 == 5:

            # capture
            if board[end_row][end_col] != "" and board[end_row][end_col].color ==self.color:
                return False
            
            board[end_row][end_col] = self
            board[start_row][start_col] = ""
            return True
        
        return False