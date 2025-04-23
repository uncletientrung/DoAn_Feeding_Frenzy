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
from classes.gameover import GameOver

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

        self.running = True
        self.game_over = False
        self.image_game_over = pygame.image.load("assets/images/GameOver.png") # Chữ GAME OVER
        # self.image_game_over = pygame.transform.scale(self.image_game_over, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

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


    def trigger_game_over(self):
        self.running = False
        self.game_over = True
        self.player.data = self.scoreBar.data
        return self.show_text_GameOver()
    
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

    def show_text_GameOver(self):
        self.screen.blit(self.image_game_over, (self.SCREEN_WIDTH // 2 - 500, self.SCREEN_HEIGHT // 2-200))
        pygame.display.flip()
        
        if self.music:
            self.sound_music_game.stop()
            self.sound_death.play()
            pygame.time.delay(1000)
            self.sound_game_over2.play()        
            self.clock.tick(self.FPS)
            print(111)
        return self.run_game_over()

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
        self.player.draw(self.screen)
        self.draw_fish_level(self.player)
        self.scoreBar.draw(self.screen, self.player)

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
    # def handle_events(self):
    #     if self.game_over:
    #         return self.show_text_GameOver()

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.running = False
    #             self.player.release_camera()
    #             return "exit"
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_SPACE:
    #                 self.player.dash()
    #             elif event.key == pygame.K_b:
    #                 self.spawn_boom()
    #             elif event.key == pygame.K_c:
    #                 self.create_boss()

        # self.player.start_cooldown()
        # return self.running

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
                        self.running = False
                        self.player.release_camera()
                        return "menu"
            if not self.game_over:           
                self.update()
                self.draw()
            self.clock.tick(self.FPS)
            
        
        return self.tham_so_game_over # Trả về kết quả game over
