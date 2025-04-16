import pygame
import time
pygame.mixer.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 680
BACKGROUND_COLOR = (0, 0, 0)

FPS = 120

PLAYER_SPEED = 5

IMAGE_PATH = "assets/images/"
SOUND_PATH = "assets/sounds/"
sound_game_over = pygame.mixer.Sound(SOUND_PATH + "gameover.wav")
sound_game_over2 = pygame.mixer.Sound(SOUND_PATH + "GameOver2.wav")
sound_death = pygame.mixer.Sound(SOUND_PATH + "die.wav")
sound_level_up = pygame.mixer.Sound(SOUND_PATH + "levelUp.wav")
sound_bubble = pygame.mixer.Sound(SOUND_PATH + "underWater.wav")
sound_boom = pygame.mixer.Sound(SOUND_PATH + "soundboom.wav")

ENEMY_FISH_TYPES = [
    ("Fishright10.png", "Fishleft10.png", 1, 0, 10, 5),
    ("Fishright2.png", "Fishleft2.png", 2, 0, 11, 10),
    ("Fishright1.png", "Fishleft1.png", 5, 0, 15, 15),
    ("Fishright3.png", "Fishleft3.png", 8, 0, 99, 20),
    ("Fishright4.png", "Fishleft4.png", 11, 6, 99, 30),
    ("Fishright5.png", "Fishleft5.png", 13, 9, 99, 50),
    ("Fishright6.png", "Fishleft6.png", 15, 12, 99, 60),
    ("Fishright7.png", "Fishleft7.png", 17, 14, 99, 80),
    ("Fishright8.png", "Fishleft8.png", 19, 16, 99, 100),
    ("Fishright9.png", "Fishleft9.png", 21, 18, 99, 150),
    ("sharkleft1.png", "shark1.png", 0, 1, 99, 5)
]

def update_fish(choice_fish):
    if choice_fish == 1:
        images_fish = {
            "left_down": pygame.image.load(IMAGE_PATH + "fish1_left_down.png"),
            "left_up": pygame.image.load(IMAGE_PATH + "fish1_left_up.png"),
            "right": pygame.image.load(IMAGE_PATH + "fish1_right.png"),
            "down": pygame.image.load(IMAGE_PATH + "fish1_down.png"),
            "left": pygame.image.load(IMAGE_PATH + "fish1_left.png"),
            "up": pygame.image.load(IMAGE_PATH + "fish1_up.png"),
            "right_down": pygame.image.load(IMAGE_PATH + "fish1_right_down.png"),
            "right_up": pygame.image.load(IMAGE_PATH + "fish1_right_up.png")
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
            "right_up": pygame.image.load(IMAGE_PATH + "fish2_right_up.png")
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
            "right_up": pygame.image.load(IMAGE_PATH + "fish3_right_up.png")
        }

def update_background(choice_background):
    try:
        if choice_background == 1:
            images_background = pygame.image.load(IMAGE_PATH + "bg11.jpg")
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