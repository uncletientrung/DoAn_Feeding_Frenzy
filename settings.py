
import pygame
import time
pygame.mixer.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 680

FPS = 60

PLAYER_SPEED = 5

IMAGE_PATH = "/assets/images/"
SOUND_PATH = "/assets/sounds/"
sound_game_over = pygame.mixer.Sound(SOUND_PATH + "gameover.wav")
sound_game_over2= pygame.mixer.Sound(SOUND_PATH + "GameOver2.wav")
sound_death = pygame.mixer.Sound(SOUND_PATH + "die.wav")
sound_level_up = pygame.mixer.Sound(SOUND_PATH + "levelUp.wav")
sound_bubble = pygame.mixer.Sound(SOUND_PATH + "underWater.wav")
sound_boom=pygame.mixer.Sound(SOUND_PATH+"soundboom.wav")

# ENEMY_FISH_TYPES = [
#     # (ảnh nhỏ, ảnh to, size, min_level_required, max_level_appear)
#     ("Fishright10.png", "Fishleft10.png", 1, 0, 10),  # Loại 1: xuất hiện từ level 0-7
#     ("Fishright2.png", "Fishleft2.png", 2, 0, 11),    # Loại 2: xuất hiện từ level 0-8
#     ("Fishright1.png", "Fishleft1.png", 5, 0, 15),    # Loại 3: xuất hiện từ level 0-9
#     ("Fishright3.png", "Fishleft3.png", 8, 0, 99),   # Loại 4: xuất hiện từ level 3-10
#     ("Fishright4.png", "Fishleft4.png", 11, 6, 99),   # Loại 5: xuất hiện từ level 4-11
#     ("Fishright5.png", "Fishleft5.png", 13, 9, 99),   # Loại 6: xuất hiện từ level 5-12
#     ("Fishright6.png", "Fishleft6.png", 15, 12, 99),   # Loại 7: xuất hiện từ level 7-13
#     ("Fishright7.png", "Fishleft7.png", 17, 14, 99),   # Loại 8: xuất hiện từ level 8-14
#     ("Fishright8.png", "Fishleft8.png", 19, 16, 99),   # Loại 9: xuất hiện từ level 9-15
#     ("Fishright9.png", "Fishleft9.png", 21, 18, 99), # Loại 10: xuất hiện từ level 10+
#     ("sharkleft1.png", "shark1.png", 0, 1, 99)     # Cá mập: xuất hiện từ level 14+
# ]
ENEMY_FISH_TYPES = [
    # (ảnh nhỏ, ảnh to, size, min_level_required, max_level_appear, điểm)
    ("Fishright10.png", "Fishleft10.png", 1, 0, 10,5),  # Loại 1: xuất hiện từ level 0-7
    ("Fishright2.png", "Fishleft2.png", 2, 0, 11,10),    # Loại 2: xuất hiện từ level 0-8
    ("Fishright1.png", "Fishleft1.png", 5, 0, 15,15),    # Loại 3: xuất hiện từ level 0-9
    ("Fishright3.png", "Fishleft3.png", 8, 0, 99,20),   # Loại 4: xuất hiện từ level 3-10
    ("Fishright4.png", "Fishleft4.png", 11, 6, 99,30),   # Loại 5: xuất hiện từ level 4-11
    ("Fishright5.png", "Fishleft5.png", 13, 9, 99,50),   # Loại 6: xuất hiện từ level 5-12
    ("Fishright6.png", "Fishleft6.png", 15, 12, 99,60),   # Loại 7: xuất hiện từ level 7-13
    ("Fishright7.png", "Fishleft7.png", 17, 14, 99,80),   # Loại 8: xuất hiện từ level 8-14
    ("Fishright8.png", "Fishleft8.png", 19, 16, 99,100),   # Loại 9: xuất hiện từ level 9-15
    ("Fishright9.png", "Fishleft9.png", 21, 18, 99,150), # Loại 10: xuất hiện từ level 10+
    ("sharkleft1.png", "shark1.png", 0, 1, 99,5)     # Cá mập: xuất hiện từ level 14+
]

