import pygame
import time
from settings import *
from classes.enemy_fish import *
from classes.main_fish import *


class Boom:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.image=pygame.image.load(IMAGE_PATH+"boom.png")
        self.base_size=SCREEN_WIDTH//7
        self.image=pygame.transform.scale(self.image,(self.base_size,self.base_size))
        self.speed=4
        self.exploded = False  # trạng thái bom nổ
        self.time=0         # Thời gian để xóa bom

    
    def move_boom(self):
        if self.y <600:
            self.y+=self.speed
    def change_when_kick(self): # Đổi hình ảnh sau khi chạm cá
            new_image = pygame.image.load(IMAGE_PATH + "kick_boom.png")
            self.image = pygame.transform.scale(new_image, (self.base_size, self.base_size))
    def draw(self,screen):# Vẽ cá lên màn hình
        if self.image:
            screen.blit(self.image,(self.x,self.y))

    def remove_boom(self): # Sau va chạm Xóa boom trong x thời gian
        if self.exploded is True and pygame.time.get_ticks()-self.time >100:
            return True
        return False
    def kick_enemy(self,enemies): # hàm kiểm tra va chạm với cá enemy
        boom_mask=pygame.mask.from_surface(self.image)
        for enemy in enemies[:]:
            enemy:EnemyFish # Python ngu nên không nhận dạng được enemy là EnemyFish nên gán
            enemy_mask=pygame.mask.from_surface(enemy.image)
            enemy_offset=(enemy.x-self.x, enemy.y-self.y)
            if boom_mask.overlap(enemy_mask,enemy_offset):
                enemies.remove(enemy)
                sound_boom.play()
                self.change_when_kick()
                self.exploded = True
                self.time = pygame.time.get_ticks() # Thời gian này cập nhập mục đích để cho nó chuyển ảnh rồi mới xóa boom
    def kick_mainfish(self,player):  # hàm kiểm tra va chạm với cá main
        player:MainFish
        boom_mask=pygame.mask.from_surface(self.image)
        player_mask=pygame.mask.from_surface(player.image)
        player_offset=(player.x - self.x,player.y -self.y )
        if boom_mask.overlap(player_mask,player_offset):
            sound_boom.play()
            if not self.exploded:
                self.change_when_kick()  # Gọi hàm explode() thay vì thay đổi ảnh trực tiếp
                self.exploded = True
                self.explosion_time = pygame.time.get_ticks() # Thời gian này cập nhập mục đích để cho nó chuyển ảnh rồi mới thua game
            return True
        return False

                

    