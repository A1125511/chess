#piece_view.py
import pygame
import os

class Pieces_view:
    def __init__(self, lattice_num, width, height):
        self.pieces = {}
        self.lattice_num = lattice_num
        self.width = width
        self.height = height
        self.load_pieces()

    def load_pieces(self):
        colors = ['w', 'b']
        pieces_types = ['B', 'K', 'N', 'p', 'Q', 'R']
        
        image_size = self.width // self.lattice_num 

        for color in colors:
            for piece in pieces_types:
                pieces_name = f'{color}{piece}'
                image_path = os.path.join('Pieces', f"{pieces_name}.png")
                try:
                    image = pygame.image.load(image_path).convert_alpha()
                    self.pieces[pieces_name] = pygame.transform.scale(image, (image_size, image_size))
                except pygame.error as e:
                    print(f"Error loading image {image_path}: {e}")

    def draw_pieces(self, screen, board, is_white_perspective, picked_up, selected_piece=None):
        pos = self.width // len(board)
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                if piece != '':
                    if isinstance(piece, str):
                        key = piece
                    else:
                        key = f'{piece.color}{piece.name}'
                    piece_name = self.pieces.get(key)
                    if is_white_perspective:
                        screen.blit(piece_name, (col * pos, row * pos))
                    else:
                        screen.blit(piece_name, ((self.lattice_num - 1 - col) * pos, (self.lattice_num - 1 - row) * pos))
        
        if selected_piece:
            r, c = picked_up
            board[r][c] = ''
            mouseX, mouseY = pygame.mouse.get_pos()
            if isinstance(selected_piece, str):
                key = selected_piece
            else:
                key = f'{selected_piece.color}{selected_piece.name}'
            
            if key in self.pieces:
                screen.blit(self.pieces[key], (mouseX - pos // 2, mouseY - pos // 2))

