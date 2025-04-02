import pygame
import sys
from settings import *
from classes import main_fish

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Màu đỏ đậm, không trong suốt

class ScoreBar:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.image = pygame.image.load(IMAGE_PATH + "Fishright11.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.font = pygame.font.SysFont("Arial", 24, bold=True)  # Thêm chữ đậm cho rõ
        self.border_width = 2  # Độ dày viền
        
    def draw(self, screen, player):
        self.level = player.level
        self.score = player.score
        size = player.size
        size_old = player.size_old + 1
        tyle_width = 1 - (size_old - size)  # Tìm tỉ lệ chiếm bao nhiêu phần trên thanh
        
        # Vẽ vòng tròn bao quanh hình con cá
        pygame.draw.circle(screen, BLACK, (40, 40), 30, 2)
        # Vẽ hình con cá trong vòng tròn
        screen.blit(self.image, (15, 15))
        
        # Thanh năng lượng
        bar_width = 150
        bar_height = 20
        bar_x, bar_y = 80, 30
        
        # Tính toán phần bên trong (không bao gồm viền)
        inner_width = bar_width - 2 * self.border_width
        inner_height = bar_height - 2 * self.border_width
        inner_x = bar_x + self.border_width
        inner_y = bar_y + self.border_width
        
        # Vẽ nền thanh năng lượng (màu trắng) - phần bên trong
        pygame.draw.rect(screen, WHITE, (inner_x, inner_y, inner_width, inner_height))
        
        # Vẽ viền đen xung quanh
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), self.border_width)
        
        # Vẽ phần progress (đảm bảo không vượt quá phần bên trong)
        progress_width = inner_width * tyle_width
        pygame.draw.rect(screen, RED, (inner_x, inner_y, progress_width, inner_height))
        
        # Hiển thị chữ "Level:" phía trên thanh năng lượng
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        screen.blit(level_text, (80, 3)) 
        
        # Hiển thị chữ "Score:" phía dưới thanh năng lượng
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (80, 47))