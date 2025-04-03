import pygame
import random
import cv2
# import mediapipe as mp
import numpy as np
import os
import time
from settings import *
from classes.main_fish import MainFish
from classes.enemy_fish import EnemyFish
from classes.bomb import Boom
from classes.bonuslv import BonusLv
from classes.boss_fish import BossFish
from classes.ScoreBar import ScoreBar

os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Feeding Frenzy")

# Load background
background = pygame.image.load(IMAGE_PATH + "bg11.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#tao font chu
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 15)

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
# pygame.mixer.music.play(-1)  

# Tạo cá chính
player = MainFish(400, 300)
scoreBar= ScoreBar()

enemy_fishes = []  
MAX_ENEMIES = 10
list_boom=[]
MAX_BOOM=50
list_bonus=[]
MAX_BONUS=1
list_boss=[]
MAX_BOSS=4


thoi_gian_cuoi_cung_spawn = 0  # Lưu thời gian lần cuối spawn cá
thoi_gian_cho_doi_spawn = random.uniform(1000, 2500)  # Giãn cách spawn cá (1 - 2.5 giây)

def spawn_enemy():
    """Hàm spawn cá địch theo level của người chơi, có thời gian giãn cách"""
    global thoi_gian_cuoi_cung_spawn, thoi_gian_cho_doi_spawn
    
    current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại

    if current_time - thoi_gian_cuoi_cung_spawn < thoi_gian_cho_doi_spawn:
        return  # Nếu chưa đủ thời gian thì không spawn

    if len(enemy_fishes) < MAX_ENEMIES:
        x_position = random.choice([-50, SCREEN_WIDTH])
        y_position = random.randint(50, SCREEN_HEIGHT - 50)

        # Kiểm tra khoảng cách để tránh spawn cá dính chùm
        for enemy in enemy_fishes:
            if abs(enemy.y - y_position) < 50:  # Nếu cá quá gần nhau (50px), chọn lại vị trí
                y_position = random.randint(50, SCREEN_HEIGHT - 50)

        new_enemy = EnemyFish(x_position, y_position, player.level)
        enemy_fishes.append(new_enemy)

        thoi_gian_cuoi_cung_spawn = current_time  # Cập nhật thời gian spawn cá
        thoi_gian_cho_doi_spawn = random.uniform(1000, 2500)  # Reset thời gian spawn ngẫu nhiên
def spawn_boom():
    if len(list_boom)<MAX_BOOM:
        x_position = random.randint(100, SCREEN_WIDTH-100)
        new_boom=Boom(x_position,-30)
        list_boom.append(new_boom)
def create_bonus():
    if len(list_bonus)<MAX_BONUS:
        x_position = random.randint(100, SCREEN_WIDTH-100)
        new_bonus=BonusLv(x_position,-30)
        list_bonus.append(new_bonus)
def create_boss():
    if len(list_boss)<MAX_BOSS:
        x_position=random.choice([-50,SCREEN_WIDTH])
        y_position=random.randint(50,SCREEN_HEIGHT-50)
        new_BossFish=BossFish(x_position,y_position)
        list_boss.append(new_BossFish)
        

running = True
clock = pygame.time.Clock()
spawn_timer = 0
last_bubble_time = time.time() # Thời gian để spawn cá mới
spawn_boom_timer=0


# vong lap while dieu khien bang phim
while running:
    current_time = time.time()
    if current_time - last_bubble_time >= 7:  # Mỗi 7 giây
        sound_bubble.play()
        last_bubble_time = current_time
    screen.blit(background, (0, 0))  # Vẽ background
    keys = pygame.key.get_pressed()
    player.move1(keys)
    player.check_collision(enemy_fishes)  # Kiểm tra va chạm với cá địch
    player.draw(screen)
    draw_fish_level(screen, player)

    # Vẽ bảng Score
    scoreBar.draw(screen,player)

    if player.eat_count == 0:  
        for _ in range(2):  
            spawn_enemy()
    
    if pygame.time.get_ticks() - spawn_timer > 2000: 
        spawn_enemy()
        spawn_timer = pygame.time.get_ticks()  
    # Hàm vẽ cá và vẽ lv trên đầu cá enemy
    for enemy in enemy_fishes:
        enemy.move(player)
        enemy.draw(screen)
        draw_enemy_level(screen, enemy)
    # Sinh ra Bonus khi random đúng số
    if random.randint(1,2000)==3 and player.level >=7:
        create_bonus()
    for bonus in list_bonus[:]:
        bonus:BonusLv
        bonus.draw_bonus(screen)
        bonus.move_bonus()
        if bonus.check_collision_main(player):
            list_bonus.remove(bonus)


    # Hàm sinh ra boom ở cấp 7
    if player.level >=7:
        if pygame.time.get_ticks() - spawn_boom_timer >20000:
            spawn_boom()
            spawn_boom_timer=pygame.time.get_ticks()

    # Hàm sinh ra cá boss
    if player.level > 7 and random.randint(1,1500)==3:
        create_boss()
    for boss in list_boss[:]:
        boss:BossFish
        boss.draw(screen)
        boss.move_boss()
        if boss.remove_boss():
            list_boss.remove(boss)
        if boss.check_collision_mainfish(player):# Kiểm tra va chạm cá chính với boss
            player.game_over()
        boss.check_colistion_enemy(enemy_fishes) # Kiểm tra boss va chạm cá enemy

            
    # Kiểm tra va chạm bom với cá chính, cá enemy
    for b in list_boom[:]:
        b:Boom
        b.draw(screen) # Vẽ bom
        b.move_boom()  # Cho bom di chuyển
        b.kick_enemy(enemy_fishes) # kiểm tra va chạm list boom với list cá enemy
        b.kick_boss(list_boss)
        
        if b.kick_mainfish(player):
            if b.changed_when_mainkick():
                # player.game_over()
                print(b.time_create)
                print(b.time_cham_Xoa)
        if b.remove_boom():
            list_boom.remove(b)


    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


#vong lap while dieu khien bang tay

#khoi tao media
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# mp_draw = mp.solutions.drawing_utils
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS, 40)
# last_x=0;
# positions = []  # Danh sách lưu vị trí trung bình
# BUFFER_SIZE = 5
# while running:
#     current_time = time.time()
#     if current_time - last_bubble_time >= 7:
#         sound_bubble.play()
#         last_bubble_time = current_time

#     screen.blit(background, (0, 0))

#     detected_tay = False  # Mặc định là không thấy tay
#     ret, frame = cap.read()
    
#     if ret:
#         frame = cv2.flip(frame, 1)
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result = hands.process(rgb_frame)
        
#         if result.multi_hand_landmarks:
#             detected_tay = True
#             for hand_landmarks in result.multi_hand_landmarks:
#                 x_pos = hand_landmarks.landmark[8].x  
#                 y_pos = hand_landmarks.landmark[8].y  

#                 new_x = int(x_pos * SCREEN_WIDTH)
#                 new_y = int(y_pos * SCREEN_HEIGHT)

#                 # Thêm vị trí vào bộ nhớ đệm
#                 positions.append((new_x, new_y))
#                 if len(positions) > BUFFER_SIZE:
#                     positions.pop(0)  # Giữ lại BUFFER_SIZE phần tử gần nhất

#                 # Lấy trung bình để làm mượt di chuyển
#                 avg_x = int(sum(p[0] for p in positions) / len(positions))
#                 avg_y = int(sum(p[1] for p in positions) / len(positions))

#                 # Chỉ đổi hướng khi di chuyển đủ xa
#                 if abs(avg_x - last_x) > SCREEN_WIDTH * 0.05:  
#                     if avg_x > player.x:
#                         player.image = player.image_right
#                     else:
#                         player.image = player.image_left
#                     last_x = avg_x  

#                 player.x, player.y = avg_x, avg_y
#                 player.rect.topleft = (player.x, player.y)

#                 mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

# # chinh lai vi tri cua camera chut xiu
#         cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
#         cv2.moveWindow("Hand Tracking", 1000, 100)
#         cv2.imshow("Hand Tracking", frame)



#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             running = False

#     # Nếu không thấy tay, dùng phím để điều khiển, chức năng này vẫn ch chạy được, ai thấy fix dùm
#     if detected_tay:
#         player.move(0, 0)
#     else:      
#         keys = pygame.key.get_pressed()  # Lấy trạng thái phím
#         player.move1(keys)  # Di chuyển bằng phím

#     # Kiểm tra va chạm
#     player.check_collision(enemy_fishes)
#     player.draw(screen)
#     draw_fish_level(screen, player)


#     if player.eat_count == 0:
#         for _ in range(2):
#             spawn_enemy()

#     if pygame.time.get_ticks() - spawn_timer > 4000:
#         spawn_enemy()
#         spawn_timer = pygame.time.get_ticks()

#     for enemy in enemy_fishes:
#         enemy.move()
#         enemy.draw(screen)
#         draw_enemy_level(screen, enemy)


#     pygame.display.update()
#     clock.tick(FPS)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# cap.release()
# cv2.destroyAllWindows()
# pygame.quit()

