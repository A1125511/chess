# pawn.py
from piece import Piece
from game_state import GameState

class Pawn(Piece):
    en_passant_target = None
    en_passant_pawn = None
    en_passant_pawn_color = None

    def __init__(self, color, position):
        super().__init__(color, "p", position, False)

    def check_en_passant(self, start, end, color):
        if Pawn.en_passant_target == end and color != Pawn.en_passant_pawn_color:
            return True, Pawn.en_passant_target, Pawn.en_passant_pawn
        return False, Pawn.en_passant_target, Pawn.en_passant_pawn

    @staticmethod
    def set_current_en_passant(en_passant_target, pawn, color):
        Pawn.en_passant_target = en_passant_target
        Pawn.en_passant_pawn = pawn
        Pawn.en_passant_pawn_color = color  

    def check_promotion(self, board, end_row, end_col, color):
        if color == "w" and end_row == 0:
            return True
        elif color == "b" and end_row == len(board) - 1:
            return True
        return False

    def is_valid_move(self, board, start, end):
        
        start_row, start_col = start
        end_row, end_col = end
        
        direction = -1 if self.color == "w" else 1

        if start == end:
            return False
        
        #print(f"[DEBUG] start_row={start_row}, direction={direction}, start_row+direction={start_row + direction}")
        #print(f"{start} and {end}")
        #print((end_row, end_col))
        #print(f"已有 {self.en_passant}")

        # 第一次移動, 移動兩格
        if self.has_moved == False and start_col == end_col and end_row == start_row + direction * 2:
            if board[start_row + direction][start_col] == "" and board[end_row][end_col] == "":
                self.en_passant = (start_row + direction, start_col)
                # print(f"建立 {self.en_passant}")
                if not GameState.is_safe_move(board, self, start, end):
                    return False
                return True
        
        # 移動
        if start_col == end_col and end_row == start_row + direction:
            if board[end_row][end_col] == "":
                if not GameState.is_safe_move(board, self, start, end):
                    return False
                return True
        
        # 吃
        if abs(end_col - start_col) == 1 and end_row == start_row + direction:
            en_passant, target, remove_pawn = self.check_en_passant(start, end, self.color)
            
            if remove_pawn is not None:
                remove_pawn_x, remove_pawn_y = remove_pawn
            else:
                remove_pawn_x, remove_pawn_y = None, None
            
            # print(f"{self.check_en_passant(start, end,)}")
            
            if board[end_row][end_col] != "" and board[end_row][end_col].color != self.color:
                if not GameState.is_safe_move(board, self, start, end):
                    return False
                return True
            elif en_passant:
                captured_pawn_piece = board[remove_pawn_x][remove_pawn_y]

                # 手動模擬, 不依靠is_safe_move
                board[end_row][end_col] = self
                board[start_row][start_col] = ""
                board[remove_pawn_x][remove_pawn_y] = ""
                
                attacker_color = "b" if self.color == "w" else "w"
                king_pos = next((r, c) for r in range(8) for c in range(8)
                    if board[r][c] != "" and board[r][c].color == self.color and board[r][c].name == "K")
                safe = not GameState.is_square_attacked(board, king_pos, attacker_color)
                
                board[start_row][start_col] = self
                board[end_row][end_col] = ""
                if remove_pawn is not None:
                    board[remove_pawn_x][remove_pawn_y] = captured_pawn_piece

                if not safe:
                    return False
                return True
            
            # print(f"{self.check_en_passant(start, end)}")

        return False

    def move(self, board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        promotion = self.check_promotion(board, end_row, end_col, self.color)
        direction = -1 if self.color == "w" else 1

        if self.has_moved == False and start_col == end_col and end_row == start_row + direction * 2:
            self.set_current_en_passant(self.en_passant, (end_row, end_col), self.color)
        elif start_col == end_col and end_row == start_row + direction:
            self.set_current_en_passant(None, None, None)
        elif abs(end_col - start_col) == 1 and abs(end_row - start_row) == 1 and board[end_row][end_col] == "":
            en_passant, target, remove_pawn = self.check_en_passant(start, end, self.color)
            
            if remove_pawn is not None:
                remove_pawn_x, remove_pawn_y = remove_pawn
            else:
                remove_pawn_x, remove_pawn_y = None, None
            
            # print(f"吃過路兵 {target}")
            # print(f"{self.check_en_passant(start, end)}")
            board[remove_pawn_x][remove_pawn_y] = ""
            Pawn.set_current_en_passant(None, None, None)
        
        board[end_row][end_col] = self
        board[start_row][start_col] = ""

        self.has_moved = True

        if promotion:
            return "promotion"
    
    def get_attacked_squares(self, board, start):
        start_row, start_col = start
        attacked_squares = []
        direction = -1 if self.color == "w" else 1
        
        if 0 <= start_row + direction < 8 and 0 <= start_col - 1 < 8:
            attacked_squares.append((start_row + direction, start_col - 1))
        if 0 <= start_row + direction < 8 and 0 <= start_col + 1 < 8:
            attacked_squares.append((start_row + direction, start_col + 1))

        return attacked_squares
    
