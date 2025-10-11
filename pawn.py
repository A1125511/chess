# pawn.py
from piece import Piece
from rule import Rule

rule = Rule()

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "p")
        self.first_move = True

    def is_valid_move(self, board, start, end):
        
        start_row, start_col = start
        end_row, end_col = end
        
        direction = -1 if self.color == "w" else 1
        
        #print(f"[DEBUG] start_row={start_row}, direction={direction}, start_row+direction={start_row + direction}")
        #print(f"{start} and {end}")
        #print((end_row, end_col))
        #print(f"已有 {self.en_passant}")

        # 第一次移動, 移動兩格
        if self.first_move and start_col == end_col and end_row == start_row + direction * 2:
            if board[start_row + direction][start_col] == "" and board[end_row][end_col] == "":
                self.first_move = False
                self.en_passant = (start_row + direction, start_col)
                print(f"建立 {self.en_passant}")
                rule.set_current_enpassant(self.en_passant, (end_row, end_col))
                promotion = rule.check_promotion(board, end_row, end_col, self.color)
                board[end_row][end_col] = self
                board[start_row][start_col] = ""
                return True
        
        # 移動
        if start_col == end_col and end_row == start_row + direction:
            if board[end_row][end_col] == "":
                self.first_move = False
                promotion = rule.check_promotion(board, end_row, end_col, self.color)
                rule.set_current_enpassant(None, None)
                board[end_row][end_col] = self
                board[start_row][start_col] = ""
                return True
        
        # 吃
        if abs(end_col - start_col) == 1 and end_row == start_row + direction:
            en_passant, target, remove_pawn = rule.check_enpassant(start, end)
            
            if remove_pawn is not None:
                remove_pawn_x, remove_pawn_y = remove_pawn
            else:
                remove_pawn_x, remove_pawn_y = None, None
            print(f"{rule.check_enpassant(start, end)}")
            
            if board[end_row][end_col] != "" and board[end_row][end_col].color != self.color:
                promotion = rule.check_promotion(board, end_row, end_col, self.color)
                board[end_row][end_col] = self
                board[start_row][start_col] = ""
                return True    
            elif en_passant:
                print(f"吃過路兵 {target}")
                print(f"{rule.check_enpassant(start, end)}")
                board[end_row][end_col] = self
                board[start_row][start_col] = ""
                board[remove_pawn_x][remove_pawn_y] = ""
                rule.set_current_enpassant(None,None)
                return True
            
            print(f"{rule.check_enpassant(start, end)}")

        return False

    