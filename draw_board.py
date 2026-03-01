# board.py
import pygame

class DrawChessBoard:
    def __init__(self, lattice_num, width, height):
        self.width = width
        self.height = height
        self.square_size = width // lattice_num
        self.lattice_num = lattice_num

    def draw(self, screen, WHITE, DARKGRAY):
        for row in range(self.lattice_num):
            for col in range(self.lattice_num):
                if (col + row) % 2 == 0:
                    color = WHITE
                else:
                    color = DARKGRAY
                pygame.draw.rect(screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))
    
    def marked_draw(self, screen, marked_positions,is_white_perspective, radius):
        for pos in marked_positions:
            if is_white_perspective:
                row, col = pos
            else:
                row, col = self.lattice_num - 1 - pos[0], self.lattice_num - 1 - pos[1]
            center = (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2)
            pygame.draw.circle(screen, (192, 255, 192), center, radius, 5)
    
    def valid_path_draw(self, screen, valid_path, board, is_white_perspective):
        for pos in valid_path:
            has_piece = board[pos[0]][pos[1]] != ""
            if is_white_perspective:
                row, col = pos
            else:
                row, col = self.lattice_num - 1 - pos[0], self.lattice_num - 1 - pos[1]
            if has_piece:
                x = col * self.square_size
                y = row * self.square_size
                rect = (x, y, self.square_size, self.square_size)
                pygame.draw.rect(screen, (192, 255, 192), rect, 5)
            else:
                center = (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2)
                pygame.draw.circle(screen, (192, 255, 192), center, 10, 0)
            

    def draw_coordinates(self, screen, is_white_perspective, WHITE, DARKGRAY):
        font = pygame.font.SysFont("Arial", 20)
        col_coordinates = [chr(97 + i) for i in range(8)]
        row_coordinates = [str(i) for i in range(8, 0, -1)]
        if not is_white_perspective:
            row_coordinates.reverse()
            col_coordinates.reverse()
        for row in range(len(row_coordinates)):
            x = 0
            y = row * self.square_size
            text = font.render(f"{row_coordinates[row]}", True, (0, 0, 0))
            screen.blit(text, (x, y))
        for col in range(len(col_coordinates)):
            x = col * self.square_size + self.square_size - 10
            y = self.height - 25
            text = font.render(f"{col_coordinates[col]}", True, (0, 0, 0))
            screen.blit(text, (x, y))
