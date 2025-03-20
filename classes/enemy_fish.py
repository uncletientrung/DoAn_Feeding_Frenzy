import pygame
import random
import math
from settings import *

class EnemyFish:
    def __init__(self, x, y, player_level):
        self.player_level = player_level  

        # Chọn cá phù hợp với level hiện tại
        valid_fish = [fish for fish in ENEMY_FISH_TYPES 
                 if fish[3] <= self.player_level and fish[4] > self.player_level]
    
        if not valid_fish:  # Nếu không có cá phù hợp, lấy các loại cao nhất
            valid_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] <= self.player_level]
    
        fish_right, fish_left, self.size, self.fish_level, _ = random.choice(valid_fish)

        self.image_right = pygame.image.load(IMAGE_PATH + fish_right)
        self.image_left = pygame.image.load(IMAGE_PATH + fish_left)

      
        base_size = SCREEN_WIDTH // 15  # Kích thước mặc định
        scale_factor = 1 + (self.size - 1) * 0.2  # Tăng kích thước theo level
        new_size = (int(base_size * scale_factor), int(base_size * scale_factor))

        self.image_right = pygame.transform.scale(self.image_right, new_size)
        self.image_left = pygame.transform.scale(self.image_left, new_size)

        self.image = self.image_right  
        self.x, self.y = x, y
        base_speed =3
        self.speed = random.choice([-1, 1]) * (base_speed + 0.5 * self.fish_level)  
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        
        self.wave_amplitude = random.uniform(0.5, 0.5)  
        self.wave_speed = random.uniform(0.05, 0.1)  
        self.wave_offset = random.uniform(0, math.pi * 2)  

    

    def move(self):
        """Di chuyển cá địch với hiệu ứng nhấp nhô"""
        self.x += self.speed
        self.y += self.wave_amplitude * math.sin(self.wave_offset)
        self.wave_offset += self.wave_speed  
        self.rect.topleft = (self.x, self.y)
        if self.speed < 0:
            self.image = self.image_left
        else:
            self.image = self.image_right

        if self.x < -self.width or self.x > SCREEN_WIDTH:
            self.reset_position()

    

    def draw(self, screen):
        """Vẽ cá địch lên màn hình"""
        screen.blit(self.image, (self.x, self.y))

    def reset_position(self):
        """Reset cá và chọn cá phù hợp với level hiện tại"""
        self.x = random.choice([-self.width, SCREEN_WIDTH])  
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = random.choice([-3, 3])  

        
        self.wave_amplitude = random.uniform(0.5, 0.5)
        self.wave_speed = random.uniform(0.05, 0.1)
        self.wave_offset = random.uniform(0, math.pi * 2)

        
        valid_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] <= self.player_level and fish[4] > self.player_level]

        if not valid_fish:  
            valid_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] <= self.player_level]

        fish_right, fish_left, self.size, self.fish_level, _ = random.choice(valid_fish)

        self.image_right = pygame.image.load(IMAGE_PATH + fish_right)
        self.image_left = pygame.image.load(IMAGE_PATH + fish_left)

        
        base_size = SCREEN_WIDTH // 15  
        scale_factor = 1 + (self.size - 1) * 0.2  
        new_size = (int(base_size * scale_factor), int(base_size * scale_factor))

        self.image_right = pygame.transform.scale(self.image_right, new_size)
        self.image_left = pygame.transform.scale(self.image_left, new_size)
        self.image = self.image_left if self.speed < 0 else self.image_right


    


