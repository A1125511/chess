from piece import Piece

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, "Q")
    
    def is_valid_move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end

        dx = end_row - start_row
        dy = end_col - start_col

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

            board[end_row][end_col] = self
            board[start_row][start_col] = ""
            if start != end:
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
            
            board[end_row][end_col] = self
            board[start_row][start_col] = ""
            return True
        
        return False
