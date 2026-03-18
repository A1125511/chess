#piece_view.py
import pygame
import os
import sys

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
                    image = pygame.image.load(self.resource_path(image_path)).convert_alpha()
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


    # 打包成exe需要
    # @staticmethod 告訴 Python：「這個方法不需要 self，它只是放在類裡面的一個普通函數。」
    @staticmethod
    def resource_path(relative_path):
        # 現在是不是被 PyInstaller 打包後在執行？

        # exe 執行
        if hasattr(sys, '_MEIPASS'):
            # 檔案其實在「暫存資料夾」
            # 所以要從 _MEIPASS 找 
            base_path = sys._MEIPASS
        # 用 Python 跑
        else:
            # 就用「目前資料夾」當作基準
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)