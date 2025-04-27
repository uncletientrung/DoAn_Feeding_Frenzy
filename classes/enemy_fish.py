import pygame
import random
import math
from settings import *

class EnemyFish:
    def __init__(self, x, y, player_level, fish_type=None):
        self.player_level = player_level

        if fish_type:
            fish_right, fish_left, self.size, self.fish_level, _, self.score_enemy = fish_type
        else:
            valid_fish = [fish for fish in ENEMY_FISH_TYPES_2 
                          if fish[3] <= self.player_level and fish[4] > self.player_level]
            if not valid_fish:
                valid_fish = [fish for fish in ENEMY_FISH_TYPES_2 if fish[3] <= self.player_level]
            fish_right, fish_left, self.size, self.fish_level, _, self.score_enemy = random.choice(valid_fish)

        self.image_right = pygame.image.load(IMAGE_PATH + fish_right)
        self.image_left = pygame.image.load(IMAGE_PATH + fish_left)

        base_size = SCREEN_WIDTH // 28
        scale_factor = 1 + (self.size - 1) * 0.1
        new_size = (int(base_size * scale_factor), int(base_size * scale_factor))

        self.image_right = pygame.transform.scale(self.image_right, new_size)
        self.image_left = pygame.transform.scale(self.image_left, new_size)

        self.image = self.image_right
        self.x, self.y = x, y
        base_speed = 1.5
        if x < 0:
            self.speed = base_speed + 0.2 * (self.fish_level)*0.5
        else:
            self.speed = -(base_speed + 0.2 * ((self.fish_level)*0.5))
        # Tăng tốc độ cho cá nhỏ hơn người chơi
        if self.size < player_level:
            self.speed *= 1.5  # Tăng 50% tốc độ cho cá nhỏ
        # Giữ nguyên tốc độ cho cá mạnh hoặc bằng cấp
        elif self.size > player_level:
            self.speed *= 1  # Không tăng tốc cho cá mạnh
        self.width, self.height = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.wave_amplitude = random.uniform(0.5, 0.75)
        self.wave_speed = random.uniform(0.05, 0.1)
        self.wave_offset = random.uniform(0, math.pi * 2)
        self.khoangcach_quaydau_bo_chay = 60

    def move(self, player):
        """Di chuyển cá địch và kiểm tra nếu cần bỏ chạy hoặc đuổi theo"""
        distance = math.sqrt((player.x - self.x) ** 2 + (player.y - self.y) ** 2)
        y_distance = abs(player.y - self.y)

        if self.size < player.level and distance < self.khoangcach_quaydau_bo_chay:
            if player.x < self.x:
                self.speed = abs(self.speed)
            else:
                self.speed = -abs(self.speed)
        # elif self.size > player.level and distance < 300 and y_distance < 40:
        #     if player.x < self.x:
        #         self.speed = -abs(self.speed)
        #     else:
        #         self.speed = abs(self.speed)

        self.x += self.speed
        self.y += self.wave_amplitude * math.sin(self.wave_offset)
        self.wave_offset += self.wave_speed
        self.rect.topleft = (self.x, self.y)

        self.image = self.image_left if self.speed < 0 else self.image_right

        if self.speed > 0 and self.x > SCREEN_WIDTH:
            self.reset_position()
        elif self.speed < 0 and self.x < -self.width:
            self.reset_position()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def reset_position(self):
        self.x = random.choice([-self.width, SCREEN_WIDTH])
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        base_speed = 1.5
        if self.x < 0:
            self.speed = base_speed + 0.25 * self.fish_level
        else:
            self.speed = -(base_speed + 0.25 * self.fish_level)

          
        # Tăng tốc độ cho cá nhỏ hơn người chơi
        if self.size < self.player_level:
            self.speed *= 1.5  # Tăng 50% tốc độ cho cá nhỏ
        # Giữ nguyên tốc độ cho cá mạnh hoặc bằng cấp
        elif self.size > self.player_level:
            self.speed *= 0.9  # Không tăng tốc cho cá mạnh

        self.wave_amplitude = random.uniform(0.5, 0.75)
        self.wave_speed = random.uniform(0.05, 0.1)
        self.wave_offset = random.uniform(0, math.pi * 2)
        self.image = self.image_left if self.speed < 0 else self.image_right
        self.width, self.height = self.image.get_size()