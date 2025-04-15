import pygame
from settings import *
from classes.main_fish import *


class BonusLv:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.image=pygame.image.load(IMAGE_PATH+"kimcuong.png")
        self.size_base=SCREEN_WIDTH//25
        self.image=pygame.transform.scale(self.image,(self.size_base,self.size_base))
        self.sound=pygame.mixer.Sound(SOUND_PATH+"bonus1.wav")
        self.speed=4
    
    def move_bonus(self):
        if self.y<590:
            self.y+=self.speed
    def draw_bonus(self,screen):
        screen.blit(self.image,(self.x,self.y))
    def check_collision_main(self,player):
        player:MainFish
        bonus_mask=pygame.mask.from_surface(self.image)
        player_mask=pygame.mask.from_surface((player.image))
        player_offset=(player.x - self.x,player.y-self.y)
        if bonus_mask.overlap(player_mask,player_offset):
            self.sound.play()
            player.level+=1
            return True
        return False

