import random
import os
from datetime import datetime
from piece import Piece

MAX_FILES = 20

class GameState:
    def __init__(self):
        self.is_white_perspective = random.choice([True, False])
        self.move_history = []
        self.count = 1
        self.position_history = {}
    
    def getCurrentPlayer(self):
        return self.is_white_perspective

    def pos_to_notation(self, row, col):
        letter = chr(97 + col)
        number = str(8 - row)
        return letter + number

    def record_movement(self, board, piece, start, end, captured, special_move=None):
        #
        if special_move == "O-O" or special_move == "O-O-O":
            self.move_history.append(special_move)
        elif special_move == "promotion":
            notation = self.pos_to_notation(end[0], end[1])
            movement = notation + "=" + piece.name.upper()
            self.move_history.append(movement)
        else:
            if piece.name == "p":
                if captured:
                    start_pos = self.pos_to_notation(start[0], start[1])
                    movement = start_pos[0] + "x" + self.pos_to_notation(end[0], end[1])
                else:
                    movement = self.pos_to_notation(end[0], end[1])
            else:
                if captured:
                    movement = piece.name.upper() + "x" + self.pos_to_notation(end[0], end[1])
                else:
                    movement = piece.name.upper() + self.pos_to_notation(end[0], end[1])
            self.move_history.append(movement)
    
    def save_move_history(self, num_player):
        folder_name = "move_history"
        os.makedirs(folder_name, exist_ok=True)
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        move_history_path = os.path.join(folder_name, current_time + ".txt")

        with open(move_history_path, "w") as f:
            for move in self.move_history:
                f.write(f"{move:<6}")
                if self.count == num_player:
                    f.write("\n")
                    self.count = 1
                else:
                    f.write(" ")
                    self.count += 1
        
        files = sorted(
            [os.path.join(folder_name, f) for f in os.listdir(folder_name)],
            key=os.path.getmtime
        )

        while len(files) > MAX_FILES:
            os.remove(files[0])
            files.pop(0)
    
    def board_to_string(self, board, current_color):
        """把棋盤狀態轉成唯一字串"""
        from pawn import Pawn
        result = ""
        for row in board:
            for piece in row:
                if piece == "":
                    result += "."
                else:
                    result += piece.color + piece.name
                    if piece.name in ["K", "R"]:
                        result += str(int(piece.has_moved))
        result += current_color
        result += str(Pawn.en_passant_target)
        return result

    @staticmethod
    def is_square_attacked(board, pos, attacker_color):
        # 檢查 pos 這個格子，是否有被 attacker_color 的任何棋子攻擊
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece != "" and piece.color == attacker_color:
                    attacked_squares = piece.get_attacked_squares(board, (r, c))
                    if pos in attacked_squares:
                        # print(f"{piece.name.upper()} at ({r}, {c}) attacks {pos}")
                        return True
        return False

    @staticmethod
    def is_safe_move(board, piece, start, end):
        # 模擬移動，並檢查自己的國王是否安全
        # 1. 備份目標格子原本的東西 (可能是空的，也可能是被吃的敵方棋子)
        target_piece = board[end[0]][end[1]]
        
        # 2. 模擬移動 (純粹在陣列上搬移，不呼叫 piece.move() 以免改變 has_moved)
        board[end[0]][end[1]] = piece
        board[start[0]][start[1]] = ""
        
        # 3. 找出己方國王的位置
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = board[r][c]
                if p != "" and p.color == piece.color and p.name == "K":
                    king_pos = (r, c)
                    break
            if king_pos:
                break
                
        # 4. 檢查敵方是否攻擊我們的國王
        attacker_color = "b" if piece.color == "w" else "w"
        is_safe = not GameState.is_square_attacked(board, king_pos, attacker_color)
        
        # 5. 手動還原棋盤 (非常重要！)
        board[start[0]][start[1]] = piece
        board[end[0]][end[1]] = target_piece
        
        return is_safe

    @staticmethod
    def has_legal_move(board, color):
        # 檢查 color 方是否還有任何合法步可以走
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece != "" and piece.color == color:
                    # 嘗試這個棋子能不能走到棋盤上的任何一格
                    for end_r in range(8):
                        for end_c in range(8):
                            if piece.is_valid_move(board, (r, c), (end_r, end_c)):
                                return True  # 找到一步合法的就夠了
        return False  # 所有棋子都沒有合法步
    
    # 未完成
    @staticmethod
    def check_Insufficient_Material(board):
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece != "":
                    pass

"""
def is_square_attacked(board, pos, attacker_color):
    # 檢查 pos 這個格子，是否有被 attacker_color 的任何棋子攻擊
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            # 如果是敵方棋子
            if piece != "" and piece.color == attacker_color:
                # 取得該敵方棋子所有能攻擊的格子
                attacked_squares = piece.get_attacked_squares(board, (r, c))
                if pos in attacked_squares:
                    # print(f"{piece.name.upper()} at ({r}, {c}) attacks {pos}")
                    return True
    return False

def is_safe_move(board, piece, start, end):
    # 模擬移動，並檢查自己的國王是否安全
    # 1. 備份目標格子原本的東西 (可能是空的，也可能是被吃的敵方棋子)
    target_piece = board[end[0]][end[1]]
    
    # 2. 模擬移動 (純粹在陣列上搬移，不呼叫 piece.move() 以免改變 has_moved)
    board[end[0]][end[1]] = piece
    board[start[0]][start[1]] = ""
    
    # 3. 找出己方國王的位置
    king_pos = None
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p != "" and p.color == piece.color and p.name == "K":
                king_pos = (r, c)
                break
        if king_pos:
            break
            
    # 4. 檢查敵方是否攻擊我們的國王
    attacker_color = "b" if piece.color == "w" else "w"
    is_safe = not is_square_attacked(board, king_pos, attacker_color)
    
    # 5. 手動還原棋盤 (非常重要！)
    board[start[0]][start[1]] = piece
    board[end[0]][end[1]] = target_piece
    
    return is_safe

def has_legal_move(board, color):
    # 檢查 color 方是否還有任何合法步可以走
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "" and piece.color == color:
                # 嘗試這個棋子能不能走到棋盤上的任何一格
                for end_r in range(8):
                    for end_c in range(8):
                        if piece.is_valid_move(board, (r, c), (end_r, end_c)):
                            return True  # 找到一步合法的就夠了
    return False  # 所有棋子都沒有合法步

"""