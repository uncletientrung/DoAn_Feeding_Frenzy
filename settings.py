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
    # (ảnh nhỏ, ảnh to, size, min_level_required, max_level_appear, điểm)
ENEMY_FISH_TYPES = [
    ("Fishright10.png", "Fishleft10.png", 1, 0, 10, 5),
    ("Fishright2.png", "Fishleft2.png", 1, 0, 11, 10),
    ("Fishright1.png", "Fishleft1.png", 1, 0, 15, 15),
    ("Fishright3.png", "Fishleft3.png", 1, 0, 99, 20),
    ("Fishright4.png", "Fishleft4.png", 11, 6, 99, 30),
    ("Fishright5.png", "Fishleft5.png", 13, 9, 99, 50),
    ("Fishright6.png", "Fishleft6.png", 15, 12, 99, 60),
    ("Fishright7.png", "Fishleft7.png", 17, 14, 99, 80),
    ("Fishright8.png", "Fishleft8.png", 19, 16, 99, 100),
    ("Fishright9.png", "Fishleft9.png", 21, 18, 99, 150),
    ("sharkleft1.png", "shark1.png", 0, 1, 99, 5)
]
ENEMY_FISH_TYPES_2 = [
    # (ảnh phải, ảnh trái, size, min_level_required, max_level_appear, điểm)

    ("Fishright0.png",  "Fishleft0.png",  1, 1, 9, 5),
    ("Fishright1.png",  "Fishleft1.png",  1, 1, 9, 5),
    ("Fishright2.png",  "Fishleft2.png",  3, 1, 12, 15),
    ("Fishright3.png",  "Fishleft3.png",  4, 1, 12, 20),
    ("Fishright4.png",  "Fishleft4.png",  5, 1, 14, 25),
    ("Fishright5.png",  "Fishleft5.png",  7, 3, 17, 35),
    ("Fishright6.png",  "Fishleft6.png",  7, 5, 17, 35),
    ("Fishright7.png",  "Fishleft7.png",  8, 5, 99, 40),
    ("Fishright8.png",  "Fishleft8.png",  9, 7, 99, 45),
    ("Fishright9.png",  "Fishleft9.png", 9,7,99, 45),
    ("Fishright10.png", "Fishleft10.png",11,8,99, 55),
    ("Fishright11.png", "Fishleft11.png",13,10,99, 65),
    ("Fishright12.png", "Fishleft12.png",13,10,99, 65),
    ("Fishright13.png", "Fishleft13.png",15,13,99, 75),
    ("Fishright14.png", "Fishleft14.png",15,15,99, 75),
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