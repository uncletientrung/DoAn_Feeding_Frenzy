from turtle import Screen
import pygame
import random
import cv2
import mediapipe as mp
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
from classes.Bubble import Bubble
from classes.gameover import GameOver
from classes.mainmenu import ImageButton
SCALE = 0.5

class Game:
    def __init__(self, image_background, list_images_fish, choice_control,choice_fish,music,sound):
        self.music = music  # Âm thanh nhạc
        self.sound = sound # # Âm thanh hiệu ứng
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"
        pygame.init()
        pygame.mixer.init()
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 680
        self.FPS = 90
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Feeding Frenzy")
        self.clock = pygame.time.Clock()

        self.background = image_background
        
        self.list_images_fish = list_images_fish

        
        self.choice_fish = choice_fish  # Lưu ý: Trong mã hiện tại, tham số được truyền là choice_control, cần sửa thành choice_fish
        # Định nghĩa ánh xạ từ choice_fish sang hình ảnh hiển thị
        self.display_images = {
            1: "assets/images/fish1_hp.png",  # Hình ảnh hiển thị cho cá 1
            2: "assets/images/fish2_hp.png",  # Hình ảnh hiển thị cho cá 2
            3: "assets/images/fish3_hp.png"   # Hình ảnh hiển thị cho cá 3
        }
        # Lấy đường dẫn hình ảnh dựa trên choice_fish, nếu không có thì dùng mặc định
        self.display_image_path = self.display_images.get(self.choice_fish, "assets/images/fish1_hp.png")
        # Tải và điều chỉnh kích thước hình ảnh
        self.display_image = pygame.image.load(self.display_image_path).convert_alpha()
        self.display_image = pygame.transform.scale(self.display_image, (208, 76.7))  # Kích thước ví dụ: 100x100
        self.choice_control = choice_control

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 15)

        # pygame.mixer.music.load(SOUND_PATH + "feeding-frenzy.wav")
        self.sound_bubble = pygame.mixer.Sound(SOUND_PATH + "underWater.wav")
        self.sound_death = pygame.mixer.Sound(SOUND_PATH + "die.wav")
        self.sound_game_over2 = pygame.mixer.Sound(SOUND_PATH + "GameOver2.wav")
        self.sound_music_game = pygame.mixer.Sound(SOUND_PATH + "music_game.wav")
        if self.music: # Nếu music là True thì bật
            self.sound_music_game.play(-1)

        self.player = MainFish(400, 300, self.list_images_fish,self.sound)

        self.scoreBar = ScoreBar(self.display_image)
        self.enemy_fishes = []
        self.MAX_ENEMIES = 10
        self.list_boom = []
        self.MAX_BOOM = 50
        self.list_bonus = []
        self.MAX_BONUS = 1
        self.list_boss = []
        self.MAX_BOSS = 2

        self.last_time_spawn = 0
        self.min_spawn_interval = 30 if self.player.level <= 4 else 15 if self.player.level <= 8 else 10
        self.thoi_gian_cuoi_cung_spawn = 0
        self.thoi_gian_cho_doi_spawn = random.uniform(1000, 2500)
        self.spawn_timer = 0
        self.spawn_boom_timer = 0
        self.last_bubble_time = time.time()


        self.bubble_image = pygame.image.load("assets/images/bubble.png").convert_alpha()
        self.bubbles = []
        self.last_spawn_time = time.time()

        self.running = True
        self.game_over = False
        self.image_game_over = pygame.image.load("assets/images/GameOver.png") # Chữ GAME OVER
        # Nút pause
        space_btn=50
        self.image_text_pause = pygame.image.load("assets/images/Pause.png")
        self.image_text_pause = pygame.transform.scale(self.image_text_pause, (int(self.image_text_pause.get_width() *0.7),
                                                                                int(self.image_text_pause.get_height()* 0.7))) 
                                                                              # Ép kiểu int mới chạy
        self.btn_pause=ImageButton(self.SCREEN_WIDTH - 10 - 55, 15, "assets/button2/Pause.png", SCALE)
        self.pause_btn_status=False  # trạng thái nút dần
        self.btn_continue=ImageButton(int(self.SCREEN_WIDTH // 2 - self.btn_pause.width//2 + space_btn*6 -180),
                                       self.SCREEN_HEIGHT // 2-50,"assets/button2/Play2.png",SCALE)
                                                             
        self.btn_music=ImageButton(int(self.SCREEN_WIDTH // 2 - self.btn_pause.width//2 +space_btn*3-180),
                                    self.SCREEN_HEIGHT // 2-50, "assets/button2/Music-On.png",SCALE)
                                                             
        self.btn_sound=ImageButton(int(self.SCREEN_WIDTH // 2 - self.btn_pause.width//2 + space_btn*4.5-180),
                                    self.SCREEN_HEIGHT // 2-50, "assets/button2/Sound-One.png",SCALE)
                                                             
        self.btn_menu=ImageButton(int(self.SCREEN_WIDTH // 2 - self.btn_pause.width//2 +space_btn*1.5-180), 
                                  self.SCREEN_HEIGHT // 2-50, "assets/button2/Exit.png",SCALE)
                                                             
        self.pause_screen= None # Tạo cái này để làm biến giữ màn hình pause tạm thời

    def draw_fish_level(self, fish):
        text_surface = self.font.render(f"Lv {fish.level}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(fish.x + fish.width // 2, fish.y - 10))
        self.screen.blit(text_surface, text_rect)

    def draw_enemy_level(self, fish):
        text_surface = self.font.render(f"Lv {fish.size}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(fish.x + fish.width // 2, fish.y - 10))
        self.screen.blit(text_surface, text_rect)

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.thoi_gian_cuoi_cung_spawn < self.thoi_gian_cho_doi_spawn:
            return

        if len(self.enemy_fishes) < self.MAX_ENEMIES:
            x_position = random.choice([-50, self.SCREEN_WIDTH])
            y_position = random.randint(50, self.SCREEN_HEIGHT - 50)

            available_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] <= self.player.level <= fish[4]]
            is_strong_fish = random.randint(1, 1000) <= 10
            if is_strong_fish:
                strong_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] > self.player.level]
                if strong_fish:
                    fish_type = random.choice(strong_fish)
                else:
                    fish_type = random.choice(available_fish)
            else:
                fish_type = random.choice(available_fish)

            new_enemy = EnemyFish(x_position, y_position, self.player.level, fish_type)
            self.enemy_fishes.append(new_enemy)

            self.thoi_gian_cuoi_cung_spawn = current_time
            self.thoi_gian_cho_doi_spawn = random.uniform(1000, 2500)

    def spawn_boom(self):
        if len(self.list_boom) < self.MAX_BOOM:
            x_position = random.randint(100, self.SCREEN_WIDTH - 100)
            new_boom = Boom(x_position, -30,self.sound)
            self.list_boom.append(new_boom)

    def create_bonus(self):
        if len(self.list_bonus) < self.MAX_BONUS:
            x_position = random.randint(100, self.SCREEN_WIDTH - 100)
            new_bonus = BonusLv(x_position, -30,self.sound)
            self.list_bonus.append(new_bonus)

    def create_boss(self):
        current_time = time.time()
        if current_time - self.last_time_spawn >= self.min_spawn_interval:
            if self.player.level > 7 and BossFish.should_spawn() and len(self.list_boss) <= self.MAX_BOSS:
                new_boss = BossFish(x=0, y=random.randint(150, self.SCREEN_HEIGHT - 150))
                self.list_boss.append(new_boss)
                self.last_time_spawn = current_time
    
    def show_menu_pause(self):
        ocean_bg = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        ocean_bg.fill((0, 30, 60, 100))
        self.screen.blit(ocean_bg, (0, 0))

        self.screen.blit(self.image_text_pause, (int(self.SCREEN_WIDTH // 2 - self.image_text_pause.get_width()//2),
                                                 self.SCREEN_HEIGHT // 2-200))
        self.btn_continue.draw(self.screen)
        self.btn_menu.draw(self.screen)
        self.btn_music.draw(self.screen) 
        self.btn_sound.draw(self.screen) 


    def trigger_game_over(self):
        self.running = False
        self.game_over = True
        self.player.data = self.scoreBar.data
        return self.show_text_GameOver()
    
    def show_text_GameOver(self):
        self.screen.blit(self.image_game_over, (self.SCREEN_WIDTH // 2 - 500, self.SCREEN_HEIGHT // 2-200))
        pygame.display.flip()
        
        if self.music:
            self.sound_music_game.stop()
            self.sound_death.play()
            pygame.time.delay(1000)
            self.sound_game_over2.play()        
            self.clock.tick(self.FPS)
        else:
            pygame.time.delay(1000)  # để không bị trôi nhanh textGameover
            self.clock.tick(self.FPS)
        return self.run_game_over()
    
    def run_game_over(self):
        self.game_over_screen = GameOver(self.screen, self.player.score)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player.release_camera()
                    running = False
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.player.release_camera()
                        running = False
                        return "menu"
                result = self.game_over_screen.handle_event(event)
                if result in ["restart", "menu", "exit"]:
                    self.player.release_camera()
                    running = False
                    self.tham_so_game_over = result # Nhận kết quả chuyển đổi của menu game Over
                    return result
            self.game_over_screen.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)


    def update(self):        
        if not self.running or self.game_over:
            return
        
        current_time = time.time()
        if current_time - self.last_bubble_time >= 7:
            if self.sound: # Nếu sound là True thì bật
                self.sound_bubble.play()
            self.last_bubble_time = current_time

        keys = pygame.key.get_pressed()
        if self.choice_control == 1:
            self.player.move1(keys)
        elif self.choice_control == 2:
            self.player.move2(keys)
        elif self.choice_control == 3:
            self.FPS=60
            direction = self.player.move3()
            if direction:
                self.player.image = self.player.images[direction]

        if self.player.check_collision(self.enemy_fishes, self.scoreBar.data):
            
            return self.trigger_game_over()

        if self.player.eat_count == 0:
            for _ in range(2):
                self.spawn_enemy()
        if pygame.time.get_ticks() - self.spawn_timer > 2000:
            self.spawn_enemy()
            self.spawn_timer = pygame.time.get_ticks()

        if random.randint(1, 2000) == 3 and self.player.level >= 7:
            self.create_bonus()

        if self.player.level >= 7:
            if pygame.time.get_ticks() - self.spawn_boom_timer > 20000:
                self.spawn_boom()
                self.spawn_boom_timer = pygame.time.get_ticks()

        self.create_boss()

        for enemy in self.enemy_fishes[:]:
            enemy.move(self.player)

        for bonus in self.list_bonus[:]:
            bonus.move_bonus()
            if bonus.check_collision_main(self.player):
                self.list_bonus.remove(bonus)

        for boss in self.list_boss[:]:
            boss.move_boss()
            if boss.check_collision_mainfish(self.player):                
                return self.trigger_game_over()
            
            boss.check_colistion_enemy(self.enemy_fishes)
            if boss.remove_boss():
                self.list_boss.remove(boss)

        for b in self.list_boom[:]:
            b.move_boom()
            b.kick_enemy(self.enemy_fishes)
            b.kick_boss(self.list_boss)
            if b.kick_mainfish(self.player, self.screen):
                if b.changed_when_mainkick():
                    b.draw(self.screen)
                
                    return self.trigger_game_over()
            if b.remove_boom():
                self.list_boom.remove(b)

        if self.player.dash_start_time and time.time() - self.player.dash_start_time >= 0.2:
            self.player.end_dash()

    def draw(self):
        if self.game_over: # Viết vầy để khi nó chạy ở game over thì nó không vẽ lại game
            return
        self.screen.blit(self.background, (0, 0))

        # Vẽ hình ảnh hiển thị ở góc trên trái
        self.screen.blit(self.display_image, (10, 10))  # Vị trí (10, 10) là ví dụ
        self.btn_pause.draw(self.screen) # Vẽ nút pause ở góc trên bên phải
        self.player.draw(self.screen)
        self.draw_fish_level(self.player)
        self.scoreBar.draw(self.screen, self.player)
        current_time = time.time()
        if current_time - self.last_spawn_time >= 3:
            num_bubbles = random.randint(1, 4)  # từ 1 đến 5 bong bóng mỗi lần
            for _ in range(num_bubbles):
                self.bubbles.append(Bubble(self.bubble_image, SCREEN_WIDTH, SCREEN_HEIGHT))
            self.last_spawn_time = current_time

        for bubble in self.bubbles[:]:
            bubble.update()
            bubble.draw(self.screen)
            if bubble.is_off_screen():
                self.bubbles.remove(bubble)



        for enemy in self.enemy_fishes:
            enemy.draw(self.screen)
            self.draw_enemy_level(enemy)

        for bonus in self.list_bonus:
            bonus.draw_bonus(self.screen)

        for boss in self.list_boss:
            boss.draw(self.screen)

        for b in self.list_boom:
            b.draw(self.screen)

        if self.choice_control == 3:
            camera_surface = self.player.get_camera_surface()
            self.screen.blit(camera_surface, (1, self.SCREEN_HEIGHT - 115))

        pygame.display.update()


    def run_menu_pause(self):      
        if self.pause_screen is None: # nếu nhấn pause thì kiểm tra cái này có None không
            self.pause_surface = self.screen.copy()  # Nếu có thì sao chép screen hàm copy có sẵn nếu screen là 1 surface

        while self.pause_btn_status:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player.release_camera()
                    self.pause_surface = None  # Xóa surface tạm khi thoát
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_btn_status = False
                        self.pause_surface = None  # Xóa surface tạm khi tiếp tục
                        return "continue"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_continue.draw(self.screen):
                        self.pause_btn_status = False
                        self.pause_surface = None  # Xóa surface tạm khi tiếp tục
                        return "continue"
                    if self.btn_menu.draw(self.screen):
                        self.pause_surface = None  # Xóa surface tạm khi về menu
                        return "menu"
                    if self.btn_music.draw(self.screen):
                        self.music = not self.music
                        new_image_path = "assets/button2/Music-On.png" if self.music else "assets/button2/Music-Off.png"
                        self.btn_music.image_default = pygame.image.load(new_image_path).convert_alpha()
                        self.btn_music.image = pygame.transform.scale(self.btn_music.image_default, 
                                                                    (self.btn_music.width, self.btn_music.height))
                        if self.music: # Tắt music liền khi ấn
                            self.sound_music_game.play(-1)
                        else:
                            self.sound_music_game.stop()
                    if self.btn_sound.draw(self.screen):  # Đã sửa lỗi từ draw thành kiểm tra va chạm
                        self.sound = not self.sound
                        new_image_path = "assets/button2/Sound-One.png" if self.sound else "assets/button2/Sound-None.png"
                        self.btn_sound.image_default = pygame.image.load(new_image_path).convert_alpha()
                        self.btn_sound.image = pygame.transform.scale(self.btn_sound.image_default, 
                                                                    (self.btn_sound.width, self.btn_sound.height))
            
            # Vẽ scrren vừa copy được lên màn hình liên tục
            self.screen.blit(self.pause_surface, (0, 0))
            self.show_menu_pause()  # Vẽ menu Pause lên trên
            pygame.display.flip()
            self.clock.tick(self.FPS)
    
        return "continue"

    def run(self):
        while self.running:
            if self.game_over:
                result = self.show_text_GameOver()
                return result
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.player.release_camera()
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.dash()
                    elif event.key == pygame.K_b:
                        self.spawn_boom()
                    elif event.key == pygame.K_c:
                        self.create_boss() 
                    elif event.key == pygame.K_ESCAPE:
                        self.pause_btn_status = True
                        result = self.run_menu_pause()
                        if result == "continue":
                            self.pause_btn_status = False
                            continue
                        elif result == "menu":
                            self.music
                            self.player.release_camera()
                            return "menu"
                        elif result == "exit":
                            self.player.release_camera()
                            return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_pause.draw(self.screen):
                        self.pause_btn_status = True
                        result = self.run_menu_pause()
                        if result == "continue":
                            self.pause_btn_status = False
                            continue
                        elif result == "menu":
                            self.sound_music_game.stop()
                            self.player.release_camera()
                            return "menu"
                        elif result == "exit":
                            self.sound_music_game.stop()
                            self.player.release_camera()
                            return "exit"

            if not self.game_over and not self.pause_btn_status:
                self.update()
                self.draw()

            self.clock.tick(self.FPS)

        return self.tham_so_game_over # Trả về kết quả  của hàm  game over