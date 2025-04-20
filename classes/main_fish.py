import math
import pygame
import sys
import pygame.time
from settings import *
from PDBCUtill import DatabaseManager
import time
import random
import cv2
import mediapipe as mp
import numpy as np

class MainFish(DatabaseManager):
    def __init__(self, x, y, list_images_fish):
        super().__init__()
        base_size = SCREEN_WIDTH // 25
        self.images = list_images_fish
        self.fish_number = self.images["fish_number"]

        for direction in self.images:
            if direction != "fish_number":
                self.images[direction] = pygame.transform.scale(self.images[direction], (base_size, base_size))
        self.image = self.images["right"]
        self.x, self.y = x, y
        self.width, self.height = self.image.get_size()
        self.speed = PLAYER_SPEED
        self.score = 0
        self.size = 1
        self.size_old = 1
        self.eat_count = 0
        self.level = 9
        self.eat_sound = pygame.mixer.Sound(SOUND_PATH + "eat.wav")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.can_dash = True
        self.dash_cooldown = 1.5
        self.is_frenzy = False
        self.dash_start_time = 0
        self.data = []
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.cap = cv2.VideoCapture(0)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.camera_surface = pygame.Surface((160, 120))
        self.last_camera_update_time = 0
        self.camera_update_interval = 100

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.positions = []
        self.BUFFER_SIZE = 2
        self.max_speed = 6

    def release_camera(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()

    def check_collision(self, enemies, dataScore):
        player_mask = pygame.mask.from_surface(self.image)

        for enemy in enemies[:]:
            enemy_mask = pygame.mask.from_surface(enemy.image)
            enemy_offset = (enemy.x - self.x, enemy.y - self.y)

            if player_mask.overlap(enemy_mask, enemy_offset):
                if self.level >= enemy.size:
                    self.eat_fish(enemy)
                    self.score += enemy.score_enemy
                    enemies.remove(enemy)
                elif self.level < enemy.size:
                    self.data = dataScore
                    return True  # Signal game over
                else:
                    print(f" Cá cùng cấp, không thể ăn!")
        return False

    def grow(self, enemy_level):
        self.size += 0.1 * (1 + enemy_level * 0.1)
        if self.size >= self.size_old + 1:
            self.size_old = int(self.size) + self.size * 0.1
            self.level += 1
            pygame.mixer.Sound.play(sound_level_up)

        base_size = SCREEN_WIDTH // 25
        new_size = int(base_size * (1 + self.size * 0.07))
        max_size = SCREEN_WIDTH // 3
        new_size = min(new_size, max_size)

        for direction in self.images:
            if direction != "fish_number":
                self.images[direction] = pygame.transform.scale(
                    pygame.image.load(IMAGE_PATH + f"fish{self.fish_number}_{direction}.png"), (new_size, new_size)
                )
                print(f"fish{self.fish_number}_{direction}.png")

        self.width, self.height = new_size, new_size

    def move1(self, keys):
        current_direction = None
        diagonal_speed = self.speed / math.sqrt(2)
        if keys[pygame.K_LEFT] and self.x > 0:
            if keys[pygame.K_UP] and self.y > 0:
                self.x -= diagonal_speed
                self.y -= diagonal_speed
                current_direction = "left_up"
            elif keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
                self.x -= diagonal_speed
                self.y += diagonal_speed
                current_direction = "left_down"
            else:
                self.x -= self.speed
                current_direction = "left"
        
        elif keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            if keys[pygame.K_UP] and self.y > 0:
                self.x += diagonal_speed
                self.y -= diagonal_speed
                current_direction = "right_up"
            elif keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
                self.x += diagonal_speed
                self.y += diagonal_speed
                current_direction = "right_down"
            else:
                self.x += self.speed
                current_direction = "right"
        
        elif keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
            current_direction = "up"
        
        elif keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
            current_direction = "down"

        if current_direction:
            self.image = self.images[current_direction]

        self.rect.topleft = (self.x, self.y)

    def move2(self, keys):
        current_direction = None
        diagonal_speed = self.speed / math.sqrt(2)
        if keys[pygame.K_a] and self.x > 0:
            if keys[pygame.K_w] and self.y > 0:
                self.x -= diagonal_speed
                self.y -= diagonal_speed
                current_direction = "left_up"
            elif keys[pygame.K_s] and self.y < SCREEN_HEIGHT - self.height:
                self.x -= diagonal_speed
                self.y += diagonal_speed
                current_direction = "left_down"
            else:
                self.x -= self.speed
                current_direction = "left"

        elif keys[pygame.K_d] and self.x < SCREEN_WIDTH - self.width:
            if keys[pygame.K_w] and self.y > 0:
                self.x += diagonal_speed
                self.y -= diagonal_speed
                current_direction = "right_up"
            elif keys[pygame.K_s] and self.y < SCREEN_HEIGHT - self.height:
                self.x += diagonal_speed
                self.y += diagonal_speed
                current_direction = "right_down"
            else:
                self.x += self.speed
                current_direction = "right"

        elif keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
            current_direction = "up"

        elif keys[pygame.K_s] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
            current_direction = "down"

        if current_direction:
            self.image = self.images[current_direction]

        self.rect.topleft = (self.x, self.y)

    def move3(self):
        success, frame = self.cap.read()
        direction = None
        if not success:
            return None

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)

        frame_resized = cv2.resize(frame, (160, 120))
        frame_for_pygame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                x_pos = hand_landmarks.landmark[8].x
                y_pos = hand_landmarks.landmark[8].y

                new_x = x_pos * self.screen_width
                new_y = y_pos * self.screen_height

                self.positions.append((new_x, new_y))
                if len(self.positions) > self.BUFFER_SIZE:
                    self.positions.pop(0)

                avg_x = sum(p[0] for p in self.positions) / len(self.positions)
                avg_y = sum(p[1] for p in self.positions) / len(self.positions)

                dx = avg_x - self.x
                dy = avg_y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                threshold = 20
                if distance > threshold:
                    if distance > 0:
                        dx_norm = dx / distance
                        dy_norm = dy / distance
                    else:
                        dx_norm, dy_norm = 0, 0

                    move_x = dx_norm * self.max_speed
                    move_y = dy_norm * self.max_speed

                    self.x += move_x
                    self.y += move_y
                    self.x = max(0, min(self.x, self.screen_width - self.width))
                    self.y = max(0, min(self.y, self.screen_height - self.height))

                    if abs(dx) > abs(dy):
                        if dx > 0:
                            direction = "right"
                            if dy > threshold:
                                direction = "right_down"
                            elif dy < -threshold:
                                direction = "right_up"
                        else:
                            direction = "left"
                            if dy > threshold:
                                direction = "left_down"
                            elif dy < -threshold:
                                direction = "left_up"
                    else:
                        if dy > 0:
                            direction = "down"
                            if dx > threshold:
                                direction = "right_down"
                            elif dx < -threshold:
                                direction = "left_down"
                        else:
                            direction = "up"
                            if dx > threshold:
                                direction = "right_up"
                            elif dx < -threshold:
                                direction = "left_up"

                    if direction in self.images:
                        self.image = self.images[direction]

                self.rect.topleft = (self.x, self.y)

                frame_for_pygame = np.copy(frame_resized)
                frame_for_pygame = cv2.cvtColor(frame_for_pygame, cv2.COLOR_BGR2RGB)
                self.mp_draw.draw_landmarks(
                    frame_for_pygame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        pygame_frame = pygame.image.frombuffer(frame_for_pygame.tobytes(), (160, 120), "RGB")
        self.camera_surface.blit(pygame_frame, (0, 0))

        return direction

    def get_camera_surface(self, width=160, height=120):
        return self.camera_surface

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def eat_fish(self, enemy):
        self.eat_sound.play()
        self.grow(enemy.fish_level)
        print(f"🍽️ Đã ăn cá! Player Level: {self.level} - Enemy Level: {enemy.fish_level}")

    def dash(self):
        if not self.is_frenzy and self.can_dash:
            self.speed *= 2
            self.can_dash = False
            self.dash_start_time = time.time()

    def end_dash(self):
        if self.dash_start_time and time.time() - self.dash_start_time >= 0.2:
            self.speed /= 2
            self.dash_start_time = None
            self.start_cooldown()

    def start_cooldown(self):
        if not self.is_frenzy:
            if not self.dash_cooldown:
                self.dash_cooldown = time.time()
            elif time.time() - self.dash_cooldown >= 1.5:
                self.can_dash = True
                self.dash_cooldown = None