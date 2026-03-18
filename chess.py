# chess.py
from king import King
import pygame
import random
from board import ChessBoard
from draw_board import DrawChessBoard
from piece_view import Pieces_view
from promotion_menu import Promotion_menu
from game_state import GameState
from path_show import path_show
from rule import Rule

pygame.init()

WIDTH, HEIGHT = 600, 600
# WIDTH, HEIGHT = 504, 504
lattice_num = 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess")

WHITE = (255,255,255)
DARKGRAY = (169,169,169)
GRAY_OVERLAY = (0, 0, 0, 180)
DRAG_THRESHOLD = 5

chessboard = DrawChessBoard(lattice_num, WIDTH, HEIGHT)
pieces_view = Pieces_view(lattice_num, WIDTH, HEIGHT)
board = ChessBoard().classic_board()

rule = Rule()
game_state = GameState()
currentPlayer = game_state.getCurrentPlayer()

running = True
selected_piece = None
is_drag = False
selected_pos = None
picked_up = None
marked_positions = []
promotion_pos = None
promotion_color = None
promotion_pending = False
promotion_need = None
new_piece = None
result = None
valid_path = []
start_col, start_row = None, None
end_col, end_row = None, None
eat = False
special_move = None
num_player = 2

def get_board_position():
    mouseX, mouseY = pygame.mouse.get_pos()
    col = mouseX // (WIDTH // lattice_num)
    row = mouseY // (WIDTH // lattice_num)
    if currentPlayer:
        row, col = row, col
    else:
        row, col = 7 - row, 7 - col

    return row, col

def show_promotion_menu(color):
    """
    Docstring for show_promotion_menu
    """
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(GRAY_OVERLAY)
    screen.blit(overlay, (0, 0))

    icon_size = 100
    gap = 20
    total_width = (icon_size*4) + (gap*3)
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - icon_size) // 2

    options = []

    selected_piece = None

while running:
    for event in pygame.event.get():

        if promotion_pending and event.type == pygame.KEYDOWN:
            # print("q:Queen")
            # print("b:Bishop")
            # print("n:Knight")
            # print("r:Rook\n")
            key_name = pygame.key.name(event.key)
            new_piece = Promotion_menu.show(promotion_color, key_name)
            # print(new_piece.name)
            if new_piece:
                promotion_pending = False
                r, c = promotion_pos
                board[r][c] = new_piece
                promotion_pos = None
                promotion_color = None
                promotion_pending = False
                result = None
                game_state.record_movement(board, new_piece, (start_row, start_col), (row, col), eat, special_move)

        if not promotion_pending:

            if event.type == pygame.MOUSEBUTTONDOWN:
                marked_positions = []
                mouseX, mouseY = pygame.mouse.get_pos()
                row, col = get_board_position()                

                if event.button == 1:
                    if board[row][col] != '':
                        selected_piece = board[row][col]
                        if rule.player_turn(selected_piece.color):
                            start_row, start_col = row, col
                            is_drag = False
                            picked_up = (row, col)
                            selected_pos = (mouseX, mouseY)

                            valid_path = path_show(selected_piece, board, (start_row, start_col), (row, col))
                        else:
                            selected_piece = None    
                
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
                    valid_path = []
                    
                    mouseX, mouseY = pygame.mouse.get_pos()
                    row, col = get_board_position()
                    if 0 <= mouseX < WIDTH and 0 <= mouseY < HEIGHT:
                        if selected_piece:

                            # Under modification
                            
                            # path_show(selected_piece, board, (start_row, start_col), (row, col))
                            

                            # print(selected_piece.color)
                            valid_move = selected_piece.is_valid_move(board, (start_row, start_col), (row, col))
                            if not valid_move:
                                # print(f"\n[Movement is invalid]\n")
                                board[start_row][start_col] = selected_piece
                            else:
                                # print(f"\n[Movement is valid]\n")
                                eat = True if board[row][col] != "" else False
                                result = selected_piece.move(board, (start_row, start_col), (row, col))
                                rule.next_player()

                                if selected_piece.name == "K" and abs(col - start_col) == 2:
                                    if col - start_col == 2:
                                        special_move = "O-O"      # 王側
                                    else:
                                        special_move = "O-O-O"    # 后側
                                if special_move is None:
                                    special_move = "promotion" if result == "promotion" else None
                                if special_move != "promotion":
                                    game_state.record_movement(board, selected_piece, (start_row, start_col), (row, col), eat, special_move)
                                else:
                                    start = (start_row, start_col)
                                    end = (row, col)
                                
                                is_drag = False
                                selected_pos = None
                            
                            if result == "promotion":
                                promotion_pending = True
                                promotion_pos = (row, col)
                                promotion_color = selected_piece.color
                                board[row][col] = selected_piece
                                print(f"{selected_piece.color} 到達升變格，等待升變輸入...")
                                
                            # print(f"{selected_piece.name}")
                            # print(f"{selected_piece.initial_position}")
                            selected_piece = None
                            
                    else:
                        board[start_row][start_col] = selected_piece
                        selected_piece = None

        if event.type == pygame.QUIT:
            game_state.save_move_history(num_player)
            running = False
    
    chessboard.draw(screen, WHITE, DARKGRAY)
    chessboard.draw_coordinates(screen, currentPlayer, WHITE, DARKGRAY)
    chessboard.marked_draw(screen, marked_positions, currentPlayer, radius = WIDTH // lattice_num // 2)
    chessboard.valid_path_draw(screen, valid_path, board, currentPlayer)
    pieces_view.draw_pieces(screen, board, currentPlayer, picked_up, selected_piece)
    
    pygame.display.flip()
    
pygame.quit()