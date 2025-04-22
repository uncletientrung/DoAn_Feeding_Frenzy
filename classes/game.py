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

class Game:
    def __init__(self, image_background, list_images_fish, choice_control):
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

        
        self.choice_fish = choice_control  # Lưu ý: Trong mã hiện tại, tham số được truyền là choice_control, cần sửa thành choice_fish
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

        pygame.mixer.music.load(SOUND_PATH + "feeding-frenzy.wav")
        self.sound_bubble = pygame.mixer.Sound(SOUND_PATH + "underWater.wav")
        self.sound_death = pygame.mixer.Sound(SOUND_PATH + "die.wav")
        self.sound_game_over2 = pygame.mixer.Sound(SOUND_PATH + "GameOver2.wav")

        self.player = MainFish(400, 300, self.list_images_fish)
        self.scoreBar = ScoreBar(self.list_images_fish)
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
            new_boom = Boom(x_position, -30)
            self.list_boom.append(new_boom)

    def create_bonus(self):
        if len(self.list_bonus) < self.MAX_BONUS:
            x_position = random.randint(100, self.SCREEN_WIDTH - 100)
            new_bonus = BonusLv(x_position, -30)
            self.list_bonus.append(new_bonus)

    def create_boss(self):
        current_time = time.time()
        if current_time - self.last_time_spawn >= self.min_spawn_interval:
            if self.player.level > 7 and BossFish.should_spawn() and len(self.list_boss) <= self.MAX_BOSS:
                new_boss = BossFish(x=0, y=random.randint(50, self.SCREEN_HEIGHT - 50))
                self.list_boss.append(new_boss)
                self.last_time_spawn = current_time

    def trigger_game_over(self):
        self.running = False
        self.game_over = True
        self.player.data = self.scoreBar.data
        return self.show_game_over()

    def show_game_over(self):
        self.sound_death.play()
        pygame.time.delay(600)
        self.sound_game_over2.play()

        try:
            game_over_image = pygame.image.load("assets/buttons/bar.png")
        except FileNotFoundError:
            print(f"Không tìm thấy file bar.png trong assets/buttons!")
            self.player.release_camera()
            return "menu"

        target_width = 400
        target_height = 300
        game_over_image = pygame.transform.scale(game_over_image, (target_width, target_height))
        game_over_rect = game_over_image.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        try:
            repeat_button_image = pygame.image.load("assets/button2/button_restart-sheet1.png")
            home_button_image = pygame.image.load("assets/button2/button_fullscreen-sheet1.png")
        except FileNotFoundError:
            print(f"Không tìm thấy file Repeat-Right.png hoặc Home.png trong assets/buttons!")
            self.player.release_camera()
            return "menu"

        # Kích thước mục tiêu cho nút (giữ hình tròn)
        target_size = 80  # Kích thước cạnh của hình vuông (vì hình tròn có tỷ lệ 1:1)

        # Scale giữ tỷ lệ khung hình
        def scale_keep_aspect(image, target_size):
            orig_width, orig_height = image.get_size()
            scale_ratio = min(target_size / orig_width, target_size / orig_height)  # Giữ tỷ lệ nhỏ nhất
            new_width = int(orig_width * scale_ratio)
            new_height = int(orig_height * scale_ratio)
            return pygame.transform.scale(image, (new_width, new_height))

        repeat_button_image = scale_keep_aspect(repeat_button_image, target_size)
        home_button_image = scale_keep_aspect(home_button_image, target_size)

        # Đặt vị trí cho các nút
        repeat_button_rect = repeat_button_image.get_rect(center=(self.SCREEN_WIDTH // 2 - 60, game_over_rect.bottom + 60))
        home_button_rect = home_button_image.get_rect(center=(self.SCREEN_WIDTH // 2 + 60, game_over_rect.bottom + 60))

        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)

        top_scores = [
            {"name": "Player1", "score": 1000},
            {"name": "Player2", "score": 800},
            {"name": "Player3", "score": 600}
        ]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player.release_camera()
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if repeat_button_rect.collidepoint(event.pos):
                        self.player.release_camera()
                        return "restart"
                    if home_button_rect.collidepoint(event.pos):
                        self.player.release_camera()
                        return "menu"

            self.screen.blit(game_over_image, game_over_rect)
            your_score_text = font.render(f"Your Score: {self.player.score}", True, (255, 255, 255))
            your_score_rect = your_score_text.get_rect(center=(self.SCREEN_WIDTH // 2, game_over_rect.top - 30))
            self.screen.blit(your_score_text, your_score_rect)

            colors = [(0, 0, 0), (128, 0, 128), (0, 0, 255)]
            for i, player in enumerate(top_scores):
                top_text = small_font.render(f"{i+1}. {player['name']}: {player['score']}", True, colors[i])
                top_rect = top_text.get_rect(center=(self.SCREEN_WIDTH // 2, game_over_rect.centery + (i - 1) * 40))
                self.screen.blit(top_text, top_rect)

            self.screen.blit(repeat_button_image, repeat_button_rect)
            self.screen.blit(home_button_image, home_button_rect)

            pygame.display.flip()

        self.player.release_camera()
        return "menu"

    def update(self):
        if not self.running or self.game_over:
            return

        current_time = time.time()
        if current_time - self.last_bubble_time >= 7:
            self.sound_bubble.play()
            self.last_bubble_time = current_time

        keys = pygame.key.get_pressed()
        if self.choice_control == 1:
            self.player.move1(keys)
        elif self.choice_control == 2:
            self.player.move2(keys)
        elif self.choice_control == 3:
            self.FPS=60;
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

    # def draw(self):
    #     self.screen.blit(self.background, (0, 0))
    #     self.player.draw(self.screen)
    #     self.draw_fish_level(self.player)
    #     self.scoreBar.draw(self.screen, self.player)

    #     for enemy in self.enemy_fishes:
    #         enemy.draw(self.screen)
    #         self.draw_enemy_level(enemy)

    #     for bonus in self.list_bonus:
    #         bonus.draw_bonus(self.screen)

    #     for boss in self.list_boss:
    #         boss.draw(self.screen)

    #     for b in self.list_boom:
    #         b.draw(self.screen)

    #     if self.choice_control == 3:
            
    #         camera_surface = self.player.get_camera_surface()
    #         self.screen.blit(camera_surface, (1, self.SCREEN_HEIGHT - 115))

    #     pygame.display.update()
    def draw(self):
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
    def handle_events(self):
        if self.game_over:
            return self.show_game_over()

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

        self.player.start_cooldown()
        return self.running

    def run(self):
        while self.running:
            result = self.update()
            if result in ["restart", "menu", "exit"]:
                return result
            self.draw()
            result = self.handle_events()
            if result in ["restart", "menu", "exit"]:
                return result
            self.clock.tick(self.FPS)
            
        return "menu"