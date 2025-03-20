import pygame
import random
import cv2
import mediapipe as mp
import numpy as np
import os
from settings import *
from classes.main_fish import MainFish
from classes.enemy_fish import EnemyFish


os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Feeding Frenzy")

# Load background
background = pygame.image.load(IMAGE_PATH + "bg11.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#tao font chu
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)

def draw_fish_level(screen, fish):
    """Hiển thị level của cá trên đầu nó"""
    text_surface = font.render(f"Lv {fish.level}", True, (255, 255, 255)) 
    text_rect = text_surface.get_rect(center=(fish.x + fish.width // 2, fish.y - 10))
    screen.blit(text_surface, text_rect)

def draw_enemy_level(screen, fish):
    """Hiển thị level của cá địch trên đầu nó"""
    text_surface = font.render(f"Lv {fish.size}", True, (255, 255, 255)) 
    text_rect = text_surface.get_rect(center=(fish.x + fish.width // 2, fish.y - 10))
    screen.blit(text_surface, text_rect)

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


#khoi tao media
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)



running = True
clock = pygame.time.Clock()
spawn_timer = pygame.time.get_ticks() 
last_bubble_time = time.time() # Thời gian để spawn cá mới



# vong lap while dieu khien bang phim
# while running:
#     current_time = time.time()
#     if current_time - last_bubble_time >= 7:  # Mỗi 7 giây
#         sound_bubble.play()
#         last_bubble_time = current_time
#     screen.blit(background, (0, 0))  # Vẽ background
#     keys = pygame.key.get_pressed()

#     player.move1(keys)
#     player.check_collision(enemy_fishes)  # Kiểm tra va chạm với cá địch
#     player.draw(screen)

   
#     if player.eat_count == 0:  
        
#         for _ in range(2):  
#             spawn_enemy()

    
#     if pygame.time.get_ticks() - spawn_timer > 4000: 
#         spawn_enemy()
#         spawn_timer = pygame.time.get_ticks()  

    
#     for enemy in enemy_fishes:
#         enemy.move()  
#         enemy.draw(screen)

#     pygame.display.update()
#     clock.tick(FPS)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False


#vong lap while dieu khien bang tay
while running:
    current_time = time.time()
    if current_time - last_bubble_time >= 7:
        sound_bubble.play()
        last_bubble_time = current_time

    screen.blit(background, (0, 0))

    detected_tay = False  # Mặc định là không thấy tay
    ret, frame = cap.read()
    
    if ret:
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        
        if result.multi_hand_landmarks:
            detected_tay = True  # Khi thấy tay, bật cờ này
            for hand_landmarks in result.multi_hand_landmarks:
                x_pos = hand_landmarks.landmark[8].x  # Ngón trỏ
                y_pos = hand_landmarks.landmark[8].y  
                
                new_x = int(x_pos * SCREEN_WIDTH)
                new_y = int(y_pos * SCREEN_HEIGHT)

                # Cập nhật hướng di chuyển
                if new_x > player.x:  
                    player.image = player.image_right  # Quay phải
                elif new_x < player.x:  
                    player.image = player.image_left  # Quay trái
                
                player.x, player.y = new_x, new_y
                player.rect.topleft = (player.x, player.y)

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

# chinh lai vi tri cua camera chut xiu
        cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Hand Tracking", 1000, 100)
        cv2.imshow("Hand Tracking", frame)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

    # Nếu không thấy tay, dùng phím để điều khiển
    if detected_tay:
        player.move(0, 0)
    else:      
        keys = pygame.key.get_pressed()  # Lấy trạng thái phím
        player.move1(keys)  # Di chuyển bằng phím

    # Kiểm tra va chạm
    player.check_collision(enemy_fishes)
    player.draw(screen)
    draw_fish_level(screen, player)


    if player.eat_count == 0:
        for _ in range(2):
            spawn_enemy()

    if pygame.time.get_ticks() - spawn_timer > 4000:
        spawn_enemy()
        spawn_timer = pygame.time.get_ticks()

    for enemy in enemy_fishes:
        enemy.move()
        enemy.draw(screen)
        draw_enemy_level(screen, enemy)


    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()

