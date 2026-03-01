import random
import os
from datetime import datetime

class GameState:
    def __init__(self):
        self.is_white_perspective = random.choice([True, False])
        self.move_history = []
    
    def getCurrentPlayer(self):
        return self.is_white_perspective

    def pos_to_notation(self, row, col):
        letter = chr(97 + col)
        number = str(8 - row)
        return letter + number

    def record_movement(self, board, piece, start, end, captured, special_move=None):
        #
        if special_move == "castling":
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

    def save_move_history(self):
        folder_name = "move_history"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        move_history_path = os.path.join(folder_name, current_time + ".txt")

        with open(move_history_path, "w") as f:
            for move in self.move_history:
                f.write(move + "\n")


