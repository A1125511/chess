# chess.py
import pygame
import random
from board import ChessBoard
from draw_board import DrawChessBoard
from piece_view import Pieces_view
from promotion_menu import Promotion_menu

pygame.init()

WIDTH, HEIGHT = 504, 504
lattice_num = 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess")

WHITE = (255,255,255)
DARKGRAY = (169,169,169)
DRAG_THRESHOLD = 5

#is_white_perspective = random.choice([True, False])
is_white_perspective = True

chessboard = DrawChessBoard(lattice_num, WIDTH, HEIGHT)
pieces_view = Pieces_view(lattice_num, WIDTH, HEIGHT)
board = ChessBoard().classic_board()

running = True
selected_piece = None
is_drag = False
selected_pos = None
picked_up = None
marked_positions = []
promotion_pos = None
promotion_color = None
promotion_pending = False
new_piece = None

def get_board_position():
    mouseX, mouseY = pygame.mouse.get_pos()
    col = mouseX // (WIDTH // lattice_num)
    row = mouseY // (WIDTH // lattice_num)
    if is_white_perspective:
        row, col = row, col
    else:
        row, col = 7 - row, 7 - col

    return row, col

while running:
    for event in pygame.event.get():

        if promotion_pending and event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            new_piece = Promotion_menu.show(promotion_color, key_name)
            if new_piece:
                promotion_pending = False
                r, c = promotion_pos
                board[r][c] = new_piece
                promotion_pos = None
                promotion_color = None
                promotion_pending = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            marked_positions = []
            mouseX, mouseY = pygame.mouse.get_pos()
            row, col = get_board_position()

            if event.button == 1:
                if board[row][col] != '':
                    selected_piece = board[row][col]
                    start_row, start_col = row, col
                    is_drag = False
                    picked_up = (row, col)
                    selected_pos = (mouseX, mouseY)
            
            if event.button == 3: # not finish
                if (row, col) in marked_positions:
                    marked_positions.remove((row, col))
                else:
                    marked_positions.append((row, col))
                
        elif event.type == pygame.MOUSEMOTION:
            if selected_piece and selected_pos:
                current_pos = pygame.mouse.get_pos()
                distance = ((current_pos[0] - selected_pos[0]) ** 2 + 
                            (current_pos[1] - selected_pos[1]) ** 2) ** 0.5
                
                if distance > DRAG_THRESHOLD and not is_drag:
                    is_drag = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                row, col = get_board_position()
                if 0 <= mouseX < WIDTH and 0 <= mouseY < HEIGHT:
                    if selected_piece:
                        print(selected_piece.color)
                        result = selected_piece.is_valid_move(board, (start_row, start_col), (row, col))
                        if not result:
                            print(f"\n[Movement is invalid]\n")
                            board[start_row][start_col] = selected_piece
                        else:
                            
                            print(f"\n[Movement is valid]\n")
                            is_drag = False
                            selected_pos = None
                        
                        if result == "promotion":
                            promotion_pending = True
                            promotion_pos = (row, col)
                            promotion_color = selected_piece.color
                            board[row][col] = selected_piece
                            print(f"{selected_piece.color} 到達升變格，等待升變輸入...")
                            
                        print(f"{selected_piece.name}")
                        selected_piece = None
                        
                else:
                    board[start_row][start_col] = selected_piece
                    selected_piece = None

        if event.type == pygame.QUIT:
            running = False
    
    
    chessboard.draw(screen, WHITE, DARKGRAY)
    chessboard.marked_draw(screen, marked_positions,is_white_perspective, radius = WIDTH // lattice_num // 2) 
    pieces_view.draw_pieces(screen, board, is_white_perspective, picked_up, selected_piece)
    pygame.display.flip()
    
pygame.quit()