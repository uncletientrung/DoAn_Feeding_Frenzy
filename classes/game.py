import pygame
from settings import *
from classes.main_fish import MainFish
from classes.enemy_fish import EnemyFish
import random

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Feeding Frenzy")

# Load background
background = pygame.image.load(IMAGE_PATH + "bg1.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load âm thanh
pygame.mixer.music.load(SOUND_PATH + "feeding-frenzy.wav")
pygame.mixer.music.play(-1)  # Lặp vô tận

# Tạo cá chính & cá địch
player = MainFish(400, 300)
# Tạo danh sách cá địch với hình ảnh random
enemy_fishes = [EnemyFish(random.randint(100, 700), random.randint(50, 550)) for _ in range(10)]



running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))  # Vẽ background
    keys = pygame.key.get_pressed()

    player.move(keys)
   # player.check_collision(enemy_fishes)  # Kiểm tra ăn cá địch
    player.draw(screen)

    for enemy in enemy_fishes:
        enemy.move()
        enemy.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
