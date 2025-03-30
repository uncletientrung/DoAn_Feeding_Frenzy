import pygame
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
    frames_right = load_gif(IMAGE_PATH + "shark.gif", (SCREEN_WIDTH // 10 + 150, SCREEN_WIDTH // 10 + 50))
    frames_left = load_gif(IMAGE_PATH + "sharkleft.gif", (SCREEN_WIDTH // 10 + 150, SCREEN_WIDTH // 10 + 50))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames_index = 0
        self.speed = choice([-5, 5])  # Random speed để xác định ảnh bên trái hay phải
        if self.speed > 0: # Speed >0 thì xuất hiện từ trái ảnh trái
            self.x = -BossFish.frames_right[0].get_width()  
        else:
            self.x = SCREEN_WIDTH

    def move_boss(self):
        self.x += self.speed
        self.frames_index = (self.frames_index + 1) % len(BossFish.frames_right)

    def draw(self, screen):
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

    # def check_colistion_boom(self,booms):
    #     if self.speed > 0:
    #         boss_mask = pygame.mask.from_surface(BossFish.frames_right[self.frames_index].convert_alpha())
    #     else:                     # Convert_alpha chính xác hơn tạo hình của cá, tránh tạo mask hình vuông
    #         boss_mask = pygame.mask.from_surface(BossFish.frames_left[self.frames_index].convert_alpha())
    #     for boom in booms[:]:  
    #         boom_mask = pygame.mask.from_surface(boom.image)  
    #         boom_offset = (int(boom.x - self.x),int(boom.y - self.y)) 
    #         if boss_mask.overlap(boom_mask,boom_offset):
    #             boom.change_when_kick()
    #             return boom
    #     return None




