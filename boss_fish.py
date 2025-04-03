import pygame
import random
from random import choice
from PIL import Image, ImageSequence
from settings import *

# Load GIF một lần và resize
def load_gif(path, size):
    image = Image.open(path)
    return [ pygame.image.fromstring(frame.convert("RGBA").resize(size).tobytes(),size,"RGBA",
            )for frame in ImageSequence.Iterator(image)
    ]

class BossFish:
    # Lưu cache ảnh GIF để không load lại nhiều lần
    frames_right = load_gif(IMAGE_PATH + "shark.gif", (SCREEN_WIDTH // 12 + 150, SCREEN_WIDTH // 12 + 50))
    frames_left = load_gif(IMAGE_PATH + "sharkleft.gif", (SCREEN_WIDTH // 12 + 150, SCREEN_WIDTH // 12 + 50))

    spawn_probability = 0.1 # Xác suất xuất hiện: 10%
    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y
    #     self.frames_index = 0
    #     self.speed = choice([-5, 5])  # Random speed để xác định ảnh bên trái hay phải
    #     if self.speed > 0: # Speed >0 thì xuất hiện từ trái ảnh trái
    #         self.x = -BossFish.frames_right[0].get_width()  
    #     else:
    #         self.x = SCREEN_WIDTH

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames_index = 0
        self.speed = choice([-5, 5])  # Random speed
        self.warning_time = 180  # Thời gian hiển thị cảnh báo (3 giây)
        self.is_warning = True  # Cờ để hiển thị cảnh báo

        if self.speed > 0:
            self.x = -BossFish.frames_right[0].get_width()  # Xuất hiện từ bên trái
        else:
            self.x = SCREEN_WIDTH  # Xuất hiện từ bên phải


    # def move_boss(self):
    #     self.x += self.speed
    #     self.frames_index = (self.frames_index + 1) % len(BossFish.frames_right)

    def move_boss(self):
        if self.warning_time > 0:
            self.warning_time -= 1
        else:
            self.is_warning = False
            self.x += self.speed
        self.frames_index = (self.frames_index + 1) % len(BossFish.frames_right)

    # def draw(self, screen):
    #     if self.speed > 0:
    #         screen.blit(BossFish.frames_right[self.frames_index], (self.x, self.y))
    #     else:
    #         screen.blit(BossFish.frames_left[self.frames_index], (self.x, self.y))

    def draw(self, screen):
    # Hiển thị cảnh báo tại vị trí xuất hiện của BossFish
        if self.is_warning:
            font = pygame.font.Font(None, 74)
            warning_text = font.render("!", True, (255, 0, 0))  # Dấu chấm than màu đỏ
            
            # Xác định vị trí cảnh báo dựa trên vị trí xuất hiện của BossFish
            if self.speed > 0:  # BossFish xuất hiện từ bên trái
                warning_position = (50, self.y)  # Gần rìa trái màn hình, tại `self.y`
            else:  # BossFish xuất hiện từ bên phải
                warning_position = (SCREEN_WIDTH - 100, self.y)  # Gần rìa phải màn hình, tại `self.y`

            # Vẽ dấu chấm than tại vị trí xác định
            screen.blit(warning_text, warning_position)

        # Hiển thị BossFish sau khi cảnh báo kết thúc
        if not self.is_warning:
            if self.speed > 0:
                screen.blit(BossFish.frames_right[self.frames_index], (self.x, self.y))
            else:
                screen.blit(BossFish.frames_left[self.frames_index], (self.x, self.y))

    def remove_boss(self):
        if self.speed >0 and self.x >SCREEN_WIDTH:
            return True
        elif self.speed<0 and self.x <0:
            return True
        return False
    
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
    
    @staticmethod
    def should_spawn():
        """Kiểm tra xem BossFish có nên xuất hiện hay không dựa vào xác suất"""
        return random.random() < BossFish.spawn_probability
