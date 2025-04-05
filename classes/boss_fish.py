import pygame
import random
from random import choice
from settings import *

# Tải danh sách frame thay vì GIF
def load_frames(folder_path, count, size):
    return [pygame.transform.scale(pygame.image.load(f"{folder_path}/frame_0{i}_delay-0.03s.gif"), size) for i in range(count)]

class BossFish:
    # Tải các frame từ file thay vì GIF
    frames_right = load_frames("assets/images/shark right", 10, (SCREEN_WIDTH // 12 + 150, SCREEN_WIDTH // 12 + 50))
    frames_left = load_frames("assets/images/shark left", 10, (SCREEN_WIDTH // 12 + 150, SCREEN_WIDTH // 12 + 50))

    spawn_probability = 0.01  # Xác suất xuất hiện: 1%

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames_index = 0
        self.speed = choice([-5, 5])  # Random speed
        self.warning_time = 180  # Thời gian hiển thị cảnh báo (3 giây)
        self.is_warning = True  # Cờ để hiển thị cảnh báo
        self.image = None

        # Chọn vị trí xuất hiện dựa theo hướng di chuyển
        if self.speed > 0:  
            self.x = -BossFish.frames_right[0].get_width()  
        else:  
            self.x = SCREEN_WIDTH  

    def move_boss(self):
        if self.warning_time > 0:
            self.warning_time -= 1  
        else:
            self.is_warning = False  
            self.x += self.speed  

        # Cập nhật frame dựa trên hướng di chuyển
        if self.speed > 0:  
            self.frames_index = (self.frames_index + 1) % len(BossFish.frames_right)
            self.image = BossFish.frames_right[self.frames_index]
        else:  
            self.frames_index = (self.frames_index + 1) % len(BossFish.frames_left)
            self.image = BossFish.frames_left[self.frames_index]
    
    def check_collision_mainfish(self,player):
        if self.speed > 0:
            boss_mask = pygame.mask.from_surface(BossFish.frames_right[self.frames_index].convert_alpha())
        else:                       # Convert_alpha chính xác hơn tạo hình của cá, tránh tạo mask hình vuông
            boss_mask = pygame.mask.from_surface(BossFish.frames_left[self.frames_index].convert_alpha())
        player_mask = pygame.mask.from_surface(player.image.convert_alpha())
        player_offset = (int(player.x - self.x), int(player.y - self.y))
        if boss_mask.overlap(player_mask, player_offset):
            return True
        return  False

    def check_colistion_enemy(self,enemies):
        if self.speed > 0:
            boss_mask = pygame.mask.from_surface(BossFish.frames_right[self.frames_index].convert_alpha())
        else:                       # Convert_alpha chính xác hơn tạo hình của cá, tránh tạo mask hình vuông
            boss_mask = pygame.mask.from_surface(BossFish.frames_left[self.frames_index].convert_alpha())
        for enemy in enemies[:]:  
            enemy_mask = pygame.mask.from_surface(enemy.image)  
            enemy_offset = (int(enemy.x - self.x),int(enemy.y - self.y)) 
            if boss_mask.overlap(enemy_mask, enemy_offset): 
                enemies.remove(enemy)

    def draw(self, screen):
        if self.is_warning:
            font = pygame.font.Font(None, 74)
            warning_text = font.render("!", True, (255, 0, 0))
            warning_position = (50, self.y) if self.speed > 0 else (SCREEN_WIDTH - 100, self.y)
            screen.blit(warning_text, warning_position)
        else:
            screen.blit(self.image, (self.x, self.y))
        # Hiển thị BossFish sau khi cảnh báo kết thúc
        if not self.is_warning:
            if self.speed > 0:
                screen.blit(BossFish.frames_right[self.frames_index], (self.x, self.y))
            else:
                screen.blit(BossFish.frames_left[self.frames_index], (self.x, self.y))

    def remove_boss(self):
        return (self.speed > 0 and self.x > SCREEN_WIDTH) or (self.speed < 0 and self.x < 0)

    @staticmethod
    def should_spawn():
        return random.random() < BossFish.spawn_probability