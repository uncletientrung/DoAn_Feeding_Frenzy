from turtle import Screen
import pygame
import random
import cv2
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
from classes.top_menu import TopMenu

class Game:
    def __init__(self):
        # Thiết lập môi trường Pygame
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
        pygame.init()
        pygame.mixer.init()
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 680
        self.FPS = 120
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Feeding Frenzy")
        self.clock = pygame.time.Clock()

        # Load background
        self.background = pygame.image.load(IMAGE_PATH + "bg11.jpg")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Tạo font chữ
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 15)

        # Load âm thanh
        pygame.mixer.music.load(SOUND_PATH + "feeding-frenzy.wav")
        self.sound_bubble = pygame.mixer.Sound(SOUND_PATH + "underWater.wav")  # Giả định có file bubble.wav

        # Khởi tạo các đối tượng game
        self.player = MainFish(400, 300)
        self.top_menu = TopMenu(self.player, self.screen)
        self.scoreBar = ScoreBar()
        self.enemy_fishes = []
        self.MAX_ENEMIES = 10
        self.list_boom = []
        self.MAX_BOOM = 50
        self.list_bonus = []
        self.MAX_BONUS = 1
        self.list_boss = []
        self.MAX_BOSS = 2

        # Biến thời gian
        self.last_time_spawn = 0
        self.min_spawn_interval = 30 if self.player.level <= 4 else 15 if self.player.level <= 8 else 10
        self.thoi_gian_cuoi_cung_spawn = 0
        self.thoi_gian_cho_doi_spawn = random.uniform(1000, 2500)
        self.spawn_timer = 0
        self.spawn_boom_timer = 0
        self.last_bubble_time = time.time()

        # Biến trạng thái
        self.running = True

    def draw_fish_level(self, fish):
        """Hiển thị level của cá trên đầu nó"""
        text_surface = self.font.render(f"Lv {fish.level}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(fish.x + fish.width // 2, fish.y - 10))
        self.screen.blit(text_surface, text_rect)

    def draw_enemy_level(self, fish):
        """Hiển thị level của cá địch trên đầu nó"""
        text_surface = self.font.render(f"Lv {fish.size}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(fish.x + fish.width // 2, fish.y - 10))
        self.screen.blit(text_surface, text_rect)

    def spawn_enemy(self):
        """Hàm spawn cá địch theo level người chơi, có sự đa dạng và độ khó tăng dần"""
        current_time = pygame.time.get_ticks()
        if current_time - self.thoi_gian_cuoi_cung_spawn < self.thoi_gian_cho_doi_spawn:
            return

        if len(self.enemy_fishes) < self.MAX_ENEMIES:
            x_position = random.choice([-50, self.SCREEN_WIDTH])
            y_position = random.randint(50, self.SCREEN_HEIGHT - 50)

            # Chọn cá phù hợp với level hiện tại
            available_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] <= self.player.level <= fish[4]]

            # Thỉnh thoảng spawn cá vượt tầm để đe dọa (2% cơ hội)
            is_strong_fish = random.randint(1, 1000) <= 10
            if is_strong_fish:
                strong_fish = [fish for fish in ENEMY_FISH_TYPES if fish[3] > self.player.level]
                if strong_fish:
                    fish_type = random.choice(strong_fish)
                else:
                    fish_type = random.choice(available_fish)
            else:
                fish_type = random.choice(available_fish)

            # Tạo cá địch với thông tin fish_type
            new_enemy = EnemyFish(x_position, y_position, self.player.level, fish_type)
            self.enemy_fishes.append(new_enemy)

            self.thoi_gian_cuoi_cung_spawn = current_time
            self.thoi_gian_cho_doi_spawn = random.uniform(1000, 2500)

    def spawn_boom(self):
        """Hàm sinh bom"""
        if len(self.list_boom) < self.MAX_BOOM:
            x_position = random.randint(100, self.SCREEN_WIDTH - 100)
            new_boom = Boom(x_position, -30)
            self.list_boom.append(new_boom)

    def create_bonus(self):
        """Hàm sinh bonus"""
        if len(self.list_bonus) < self.MAX_BONUS:
            x_position = random.randint(100, self.SCREEN_WIDTH - 100)
            new_bonus = BonusLv(x_position, -30)
            self.list_bonus.append(new_bonus)

    def create_boss(self):
        """Hàm sinh BossFish dựa trên điều kiện cấp độ"""
        current_time = time.time()
        if current_time - self.last_time_spawn >= self.min_spawn_interval:
            if self.player.level > 7 and BossFish.should_spawn() and len(self.list_boss) <= self.MAX_BOSS:
                new_boss = BossFish(x=0, y=random.randint(50, self.SCREEN_HEIGHT - 50))
                self.list_boss.append(new_boss)
                self.last_time_spawn = current_time

    def update(self):
        """Cập nhật trạng thái game"""
        current_time = time.time()
        if current_time - self.last_bubble_time >= 7:  # Mỗi 7 giây
            self.sound_bubble.play()
            self.last_bubble_time = current_time

        # Di chuyển cá chính
        keys = pygame.key.get_pressed()
        self.player.move1(keys)
        self.player.check_collision(self.enemy_fishes, self.scoreBar.data,self.screen)  # Truyền self.screen vào
        if self.player.score != self.top_menu.previous_score:
            self.top_menu.update_frenzy(self.player.score)

        # Sinh cá địch
        if self.player.eat_count == 0:
            for _ in range(2):
                self.spawn_enemy()
        if pygame.time.get_ticks() - self.spawn_timer > 2000:
            self.spawn_enemy()
            self.spawn_timer = pygame.time.get_ticks()

        # Sinh bonus
        if random.randint(1, 2000) == 3 and self.player.level >= 7:
            self.create_bonus()

        # Sinh bom
        if self.player.level >= 7:
            if pygame.time.get_ticks() - self.spawn_boom_timer > 20000:
                self.spawn_boom()
                self.spawn_boom_timer = pygame.time.get_ticks()

        # Sinh boss
        self.create_boss()
    # Cập nhật cá địch
        for enemy in self.enemy_fishes[:]:
            enemy.move(self.player)
        # Cập nhật bonus
        for bonus in self.list_bonus[:]:
            bonus.move_bonus()
            if bonus.check_collision_main(self.player):
                self.list_bonus.remove(bonus)
        # Cập nhật boss
        for boss in self.list_boss[:]:
            boss.move_boss()
            if boss.check_collision_mainfish(self.player):
                self.player.data= self.scoreBar.data
                self.player.game_over(self.screen)  # Đã được sửa ở câu trả lời trước 
            boss.check_colistion_enemy(self.enemy_fishes)
            if boss.remove_boss():
                self.list_boss.remove(boss)
        # Cập nhật bom
        for b in self.list_boom[:]:
            b.move_boom()
            b.kick_enemy(self.enemy_fishes)
            b.kick_boss(self.list_boss)
            if b.kick_mainfish(self.player, self.screen):
                self.player.data= self.scoreBar.data
                self.player.game_over(self.screen)
                if b.changed_when_mainkick():
                    print(b.time_create)
                    print(b.time_cham_Xoa)
            if b.remove_boom():
                self.list_boom.remove(b)

        if self.player.dash_start_time and time.time() - self.player.dash_start_time >= 0.2: # Dash kéo dài 0.2s
            self.player.end_dash()

    def draw(self):
        """Vẽ các thành phần game lên màn hình"""
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        self.draw_fish_level(self.player)
        self.scoreBar.draw(self.screen, self.player)
        self.top_menu.draw(self.player)

        for enemy in self.enemy_fishes:
            enemy.draw(self.screen)
            self.draw_enemy_level(enemy)

        for bonus in self.list_bonus:
            bonus.draw_bonus(self.screen)

        for boss in self.list_boss:
            boss.draw(self.screen)

        for b in self.list_boom:
            b.draw(self.screen)

        pygame.display.update()

    def handle_events(self):
        """Xử lý sự kiện"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.top_menu.frenzy += 80
                    self.top_menu.update_frenzy(self.player.score+10) 
                    # Vì hàm update sẽ chỉ kích hoạt frenzy khi điểm số có sự thay đổi 
                    # nên khi dùng để test, cộng thêm 10 điểm sẽ ngay lập tức kích hoạt frenzy
                elif event.key == pygame.K_SPACE:
                    self.player.dash()
                elif event.key == pygame.K_b:
                    self.spawn_boom()
                elif event.key == pygame.K_c:
                    self.create_boss()
            elif event.type == pygame.QUIT:
                self.running = False
            return self.running
            
        self.player.end_dash()
        self.player.start_cooldown()

    def run(self):
        """Chạy vòng lặp chính của game"""
        while self.running:
            self.update()
            self.draw()
            self.running = self.handle_events()
            self.clock.tick(self.FPS)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
