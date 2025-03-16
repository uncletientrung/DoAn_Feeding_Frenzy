import pygame
import random
import math
from settings import *

class EnemyFish:
    def __init__(self, x, y):
        fish_right, fish_left = random.choice(ENEMY_FISH_IMAGES)
        self.image_right = pygame.image.load(IMAGE_PATH + fish_right)
        self.image_left = pygame.image.load(IMAGE_PATH + fish_left)

        # Resize ảnh cá địch
        new_size = (SCREEN_WIDTH // 15, SCREEN_HEIGHT // 15)  
        self.image_right = pygame.transform.scale(self.image_right, new_size)
        self.image_left = pygame.transform.scale(self.image_left, new_size)

        self.image = self.image_right  # Mặc định quay phải
        self.x, self.y = x, y
        self.speed = random.choice([-3, 3])  
        self.width, self.height = self.image.get_size()
        self.size = 1  # Kích thước ban đầu

        # 🌊 Biến để tạo hiệu ứng nhấp nhô
        self.wave_amplitude = random.uniform(0.5, 0.5) 
        
        #self.wave_amplitude = random.randint(1, 1)  # Độ dao động lên xuống
        self.wave_speed = random.uniform(0.05, 0.1)  # Tốc độ nhấp nhô
        self.wave_offset = random.uniform(0, math.pi * 2)  # Pha dao động ngẫu nhiên

    def move(self):
        """Di chuyển cá địch với hiệu ứng nhấp nhô"""
        self.x += self.speed

        # 🌊 Nhấp nhô theo hàm sin
        self.y += self.wave_amplitude * math.sin(self.wave_offset)
        self.wave_offset += self.wave_speed  # Thay đổi pha để tạo dao động liên tục

        # Nếu cá đi ra khỏi màn hình, tạo lại ở vị trí mới
        if self.x < -self.width or self.x > SCREEN_WIDTH:
            self.reset_position()

    def draw(self, screen):
        """Vẽ cá địch lên màn hình"""
        screen.blit(self.image, (self.x, self.y))

    def reset_position(self):
        """Tạo cá mới khi cá đi ra khỏi màn hình"""
        self.x = random.choice([-self.width, SCREEN_WIDTH])  # Xuất hiện ở mép trái hoặc phải
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = random.choice([-3, 3])  # Hướng di chuyển ngẫu nhiên

        # 🌊 Reset hiệu ứng nhấp nhô
        self.wave_amplitude = random.uniform(0.5, 0.5)
        self.wave_speed = random.uniform(0.05, 0.1)
        self.wave_offset = random.uniform(0, math.pi * 2)

        # Đổi hình ảnh cá ngẫu nhiên
        fish_right, fish_left = random.choice(ENEMY_FISH_IMAGES)
        self.image_right = pygame.image.load(IMAGE_PATH + fish_right)
        self.image_left = pygame.image.load(IMAGE_PATH + fish_left)
        self.image_right = pygame.transform.scale(self.image_right, (self.width, self.height))
        self.image_left = pygame.transform.scale(self.image_left, (self.width, self.height))
        self.image = self.image_left if self.speed < 0 else self.image_right
