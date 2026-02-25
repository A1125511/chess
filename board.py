# board.py
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King

class ChessBoard:
    def __init__(self):
        pass
    
    def classic_board(self):
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        def back_rank(color, row):
            return[cls(color, (row, col)) for col, cls in enumerate(piece_order)]
        
        board = [
            back_rank('b', 0),
            [Pawn('b', (1, col)) for col in range(8)],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            ['' for _ in range(8)],
            [Pawn('w', (6, col)) for col in range(8)],
            back_rank('w', 7),
        ]


        
        return board
    
    def queen_board(self):
        board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['',   '',   '',   '',   '',   '',   '',   ''],
            ['wQ', 'wQ', 'wQ', 'wQ', 'wK', 'wQ', 'wQ', 'wQ']
        ]
        return board

        