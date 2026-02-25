class Rule:
   def __init__(self):
      self.en_passant_target = None
      self.pawn = None

   def set_current_enpassant(self, en_passant_target, pawn):
      self.en_passant_target = en_passant_target
      self.pawn = pawn

   def check_enpassant(self, start, end):
      if self.en_passant_target == end:
         return True, self.en_passant_target, self.pawn
      return False, self.en_passant_target, self.pawn

   def check_promotion(self, board, end_row, end_col, color):
      if color == "w" and end_row == 0:
         return True
      elif color == "b" and end_row == len(board) - 1:
         return True
      return False
   