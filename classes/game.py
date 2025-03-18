import pygame
import random

from settings import *
from classes.main_fish import MainFish
from classes.enemy_fish import EnemyFish




pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Feeding Frenzy")

# Load background
background = pygame.image.load(IMAGE_PATH + "bg11.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load âm thanh
pygame.mixer.music.load(SOUND_PATH + "feeding-frenzy.wav")
pygame.mixer.music.play(-1)  

# Tạo cá chính
player = MainFish(400, 300)

enemy_fishes = []  
MAX_ENEMIES = 10   

def spawn_enemy():
    """Hàm spawn cá theo level hiện tại của người chơi"""
    if len(enemy_fishes) < MAX_ENEMIES:
        x_position = random.choice([-50, SCREEN_WIDTH])
        y_position = random.randint(50, SCREEN_HEIGHT - 50)

        
        valid_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] <= player.level and fish[4] > player.level]

        if not valid_fish: 
            valid_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] <= player.level]

        fish_right, fish_left, size, fish_level, _ = random.choice(valid_fish)
        new_enemy = EnemyFish(x_position, y_position, player.level)

        enemy_fishes.append(new_enemy)

running = True
clock = pygame.time.Clock()
spawn_timer = pygame.time.get_ticks() 
last_bubble_time = time.time() # Thời gian để spawn cá mới

while running:
    current_time = time.time()
    if current_time - last_bubble_time >= 7:  # Mỗi 7 giây
        sound_bubble.play()
        last_bubble_time = current_time
    screen.blit(background, (0, 0))  # Vẽ background
    keys = pygame.key.get_pressed()

    player.move(keys)
    player.check_collision(enemy_fishes)  # Kiểm tra va chạm với cá địch
    player.draw(screen)

   
    if player.eat_count == 0:  
        
        for _ in range(2):  
            spawn_enemy()

    
    if pygame.time.get_ticks() - spawn_timer > 4000: 
        spawn_enemy()
        spawn_timer = pygame.time.get_ticks()  

    
    for enemy in enemy_fishes:
        enemy.move()
        enemy.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
