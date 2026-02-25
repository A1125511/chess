from piece import Piece

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
            
            return True
        
        return False

    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        board[end_row][end_col] = self
        board[start_row][start_col] = ""
        self.has_moved = True