import pygame
import time
pygame.mixer.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 680
BACKGROUND_COLOR = (0, 0, 0)

FPS = 120

PLAYER_SPEED = 5

IMAGE_PATH = "assets/images/"
IMAGE_PATH2="assets/images2/"
SOUND_PATH = "assets/sounds/"
IMAGE_BUTTON="assets/buttons"
sound_game_over = pygame.mixer.Sound(SOUND_PATH + "gameover.wav")
sound_game_over2 = pygame.mixer.Sound(SOUND_PATH + "GameOver2.wav")
sound_death = pygame.mixer.Sound(SOUND_PATH + "die.wav")
sound_level_up = pygame.mixer.Sound(SOUND_PATH + "levelUp.wav")
sound_bubble = pygame.mixer.Sound(SOUND_PATH + "underWater.wav")
sound_boom = pygame.mixer.Sound(SOUND_PATH + "soundboom.wav")
sound_menu = pygame.mixer.Sound(SOUND_PATH + "songgio.mp3")
    # (ảnh nhỏ, ảnh to, size, min_level_required, max_level_appear, điểm)
ENEMY_FISH_TYPES = [
    ("Fishright10.png", "Fishleft10.png", 1, 0, 10, 5),
    ("Fishright2.png", "Fishleft2.png", 1, 0, 11, 10),
    ("Fishright1.png", "Fishleft1.png", 2, 0, 15, 15),
    ("Fishright3.png", "Fishleft3.png", 4, 0, 99, 20),
    ("Fishright4.png", "Fishleft4.png", 5, 6, 99, 30),
    ("Fishright5.png", "Fishleft5.png", 6, 9, 99, 50),
    ("Fishright6.png", "Fishleft6.png", 15, 12, 99, 60),
    ("Fishright7.png", "Fishleft7.png", 17, 14, 99, 80),
    ("Fishright8.png", "Fishleft8.png", 19, 16, 99, 100),
    ("Fishright9.png", "Fishleft9.png", 21, 18, 99, 150),
    ("sharkleft1.png", "shark1.png", 0, 1, 99, 5)
]
ENEMY_FISH_TYPES_2 = [
    # (ảnh phải, ảnh trái, size, min_level_required, max_level_appear, điểm)
    ("sharkleft1.png", "shark1.png", 15, 12, 99, 355),  
    ("Fishright1.png",  "Fishleft1.png",  1, 1, 6, 15),
    ("f1r.png", "f1l.png", 2, 1, 6, 30),
    ("f2r.png", "f2l.png", 2, 1, 6, 30),
    ("Fishright2.png",  "Fishleft2.png",  3, 1, 8, 45),
    ("f3r.png", "f3l.png", 3, 2, 8, 45),
    ("Fishright3.png",  "Fishleft3.png",  4, 2, 11, 60),
    ("f4r.png", "f4l.png", 4, 3, 11, 60),
    ("f6r.png", "f6l.png", 5, 3, 11, 98),
    ("Fishright4.png",  "Fishleft4.png",  5, 2, 14, 98),
    ("Fishright5.png",  "Fishleft5.png",  6, 3, 17, 135),
     ("f7r.png", "f7l.png", 6, 5, 12, 130),
    ("f9r.png", "f9l.png", 7, 5, 14, 198),
    ("Fishright6.png",  "Fishleft6.png",  8, 6, 17, 235),
    ("Fishright7.png",  "Fishleft7.png",  9, 6, 99, 280),
    ("f10r.png", "f10l.png", 10, 7, 15, 232),
    ("f11r.png", "f11l.png", 12, 9, 16, 276),
    ("f12r.png", "f12l.png", 13, 10, 17, 290),
    ("Fishright8.png",  "Fishleft8.png",  11, 8, 55, 305),
     ("f14r.png", "f14l.png", 14, 11, 19, 320),
    ("Fishright9.png",  "Fishleft9.png", 9,6,43, 345),
    ("Fishright10.png", "Fishleft10.png",1,1,7, 15),
    ("Fishright11.png", "Fishleft11.png",16,13,99, 365),
     ("f18r.png", "f18l.png", 17, 14, 99, 490),
    
]
# (ảnh phải, ảnh trái, size, min_level_required, max_level_appear, điểm)
ENEMY_FISH_TYPES_3 = [
    ("f0r.png", "f0l.png", 1, 0, 5, 5),
    ("f1r.png", "f1l.png", 1, 0, 6, 8),
    ("f2r.png", "f2l.png", 2, 1, 7, 10),
    ("f3r.png", "f3l.png", 3, 2, 8, 12),
    ("f4r.png", "f4l.png", 4, 0, 9, 14),
    ("f5r.png", "f5l.png", 5, 3, 10, 16),
    ("f6r.png", "f6l.png", 6, 4, 11, 18),
    ("f7r.png", "f7l.png", 7, 5, 12, 20),
    ("f8r.png", "f8l.png", 8, 6, 13, 24),
    ("f9r.png", "f9l.png", 9, 7, 14, 28),
    ("f10r.png", "f10l.png", 10, 8, 15, 32),
    ("f11r.png", "f11l.png", 11, 9, 16, 36),
    ("f12r.png", "f12l.png", 12, 9, 17, 40),
    ("f13r.png", "f13l.png", 13, 10, 18, 45),
    ("f14r.png", "f14l.png", 14, 11, 19, 50),
    ("f16r.png", "f16l.png", 14, 12, 20, 60),
    ("f17r.png", "f17l.png", 15, 13, 20, 70),
    ("f18r.png", "f18l.png", 16, 13, 20, 90),
]



def update_images_fish(choice_fish):
    if choice_fish == 1:
        images_fish = {
            "left_down": pygame.image.load(IMAGE_PATH + "fish1_left_down.png"),
            "left_up": pygame.image.load(IMAGE_PATH + "fish1_left_up.png"),
            "right": pygame.image.load(IMAGE_PATH + "fish1_right.png"),
            "down": pygame.image.load(IMAGE_PATH + "fish1_down.png"),
            "left": pygame.image.load(IMAGE_PATH + "fish1_left.png"),
            "up": pygame.image.load(IMAGE_PATH + "fish1_up.png"),
            "right_down": pygame.image.load(IMAGE_PATH + "fish1_right_down.png"),
            "right_up": pygame.image.load(IMAGE_PATH + "fish1_right_up.png"),
            "fish_number":1
        }
    elif choice_fish == 2:
        images_fish = {
            "left_down": pygame.image.load(IMAGE_PATH + "fish2_left_down.png"),
            "left_up": pygame.image.load(IMAGE_PATH + "fish2_left_up.png"),
            "right": pygame.image.load(IMAGE_PATH + "fish2_right.png"),
            "down": pygame.image.load(IMAGE_PATH + "fish2_down.png"),
            "left": pygame.image.load(IMAGE_PATH + "fish2_left.png"),
            "up": pygame.image.load(IMAGE_PATH + "fish2_up.png"),
            "right_down": pygame.image.load(IMAGE_PATH + "fish2_right_down.png"),
            "right_up": pygame.image.load(IMAGE_PATH + "fish2_right_up.png"),
            "fish_number":2
        }
    elif choice_fish == 3:
        images_fish = {
            "left_down": pygame.image.load(IMAGE_PATH + "fish3_left_down.png"),
            "left_up": pygame.image.load(IMAGE_PATH + "fish3_left_up.png"),
            "right": pygame.image.load(IMAGE_PATH + "fish3_right.png"),
            "down": pygame.image.load(IMAGE_PATH + "fish3_down.png"),
            "left": pygame.image.load(IMAGE_PATH + "fish3_left.png"),
            "up": pygame.image.load(IMAGE_PATH + "fish3_up.png"),
            "right_down": pygame.image.load(IMAGE_PATH + "fish3_right_down.png"),
            "right_up": pygame.image.load(IMAGE_PATH + "fish3_right_up.png"),
            "fish_number":3
        }
    return images_fish

def update_background(choice_background):
    try:
        if choice_background == 1:
            images_background = pygame.image.load(IMAGE_PATH + "bgbien1.jpg")
            print("A")
        elif choice_background == 2:
            images_background = pygame.image.load(IMAGE_PATH + "bg12.jpg")
            print("B")
        elif choice_background == 3:
            images_background = pygame.image.load(IMAGE_PATH + "bg13.jpg")
            print("A")

        images_background = pygame.transform.scale(images_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    except FileNotFoundError as e:
        print(f"Không tìm thấy file: {e}")
        images_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        images_background.fill((0, 0, 0))  # Mặc định là nền đen nếu lỗi
    return images_background