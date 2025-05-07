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
import threading
import queue

class MainFish(DatabaseManager):
   
    def __init__(self, x, y, list_images_fish,sound):
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
        self.level = 1
        self.xp = 0#tinh level
        self.max_xp = 80#tinh level
        self.eat_sound = pygame.mixer.Sound(SOUND_PATH + "eat.wav")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.can_dash = True
        self.dash_cooldown = None  # Sử dụng self.dash_cooldown, không cần dash_cooldown_start
        self.dash_start_time = None  # Đặt None thay vì 0
        self.is_dashing = False

        self.is_frenzy = False
        
        self.dash_start_time = 0
        self.data = []
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.sound= sound

        self.cap = cv2.VideoCapture(0)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
        self.cap.set(cv2.CAP_PROP_FPS, 60)  # Tăng FPS nếu webcam hỗ trợ
        self.camera_surface = pygame.Surface((160, 120))
        self.last_camera_update_time = pygame.time.get_ticks()
        self.hand_detected_time = None  # Lưu thời điểm phát hiện tay đầu tiên
        self.control_delay = 400 #0.75 giây sau khi phát hiện tay mới di chuyển cá được, tránh bỏ tay vô bất thinhf lình cá chết
        self.position_queue = queue.Queue()
        self.running = True
        self.camera_thread = threading.Thread(target=self._camera_loop)
        self.camera_thread.daemon = True
        self.camera_thread.start()

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.positions = []
        self.BUFFER_SIZE = 10  # Tăng buffer để làm mượt hơn
        self.max_speed = 8  # Tăng tốc độ tối đa
        self.last_direction = "right"  # Lưu hướng cuối cùng để giữ liên tục
       

   

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
        return False

    def grow(self, enemy_level):
        self.size += 0.15 * (1 + enemy_level * 0.1)
        if self.size >= self.size_old + 1.2:
            self.size_old = int(self.size) + self.size * 0.15
            self.level += 1
            if self.sound: # Nếu sound là True thì chạy
                pygame.mixer.Sound.play(sound_level_up)

        base_size = SCREEN_WIDTH // 25
        new_size = int(base_size * (1 + self.size * 0.2))
        max_size = SCREEN_WIDTH // 3
        new_size = min(new_size, max_size)

        for direction in self.images:
            if direction != "fish_number":
                self.images[direction] = pygame.transform.scale(
                    pygame.image.load(IMAGE_PATH + f"fish{self.fish_number}_{direction}.png"), (new_size, new_size)
                )
                

        self.width, self.height = new_size, new_size

    def gain_xp(self, enemy_level):
        if enemy_level > self.level:
            return  # Không được ăn cá mạnh hơn

        level_diff = self.level - enemy_level
        base_xp = 10

        # Càng chênh lệch thì XP càng giảm, tối đa giảm còn 30%
        multiplier = max(0.5, 1 - 0.2 * level_diff)
        gained = base_xp * multiplier

        self.xp += gained
        print(f"XP: {self.xp:.2f}/{self.max_xp}")

        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp = int(self.max_xp * 1.05)  # Càng lên cấp càng khó

            if self.sound:
                pygame.mixer.Sound.play(sound_level_up)

            # Tăng kích thước cá mỗi lần lên cấp
            self.size += 0.5
            base_size = SCREEN_WIDTH // 25
            new_size = int(base_size * (1 + self.size * 0.08))
            max_size = SCREEN_WIDTH // 3
            new_size = min(new_size, max_size)

            for direction in self.images:
                if direction != "fish_number":
                    self.images[direction] = pygame.transform.scale(
                        pygame.image.load(IMAGE_PATH + f"fish{self.fish_number}_{direction}.png"),
                        (new_size, new_size)
                    )

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

    def _camera_loop(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(frame_rgb)

            # frame_resized = cv2.resize(frame, (160, 120))
            # frame_for_pygame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            #vẽ khung tay
            frame_resized = cv2.resize(frame, (160, 120))
            frame_for_pygame = np.copy(frame_resized)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame_for_pygame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )

            # Chuyển sang RGB cho pygame
            frame_for_pygame = cv2.cvtColor(frame_for_pygame, cv2.COLOR_BGR2RGB)
            pygame_frame = pygame.image.frombuffer(frame_for_pygame.tobytes(), (160, 120), "RGB")
            self.camera_surface.blit(pygame_frame, (0, 0))


            if result.multi_hand_landmarks:
                if self.hand_detected_time is None:
                    self.hand_detected_time = pygame.time.get_ticks()
                for hand_landmarks in result.multi_hand_landmarks:
                    x_pos = hand_landmarks.landmark[8].x
                    y_pos = hand_landmarks.landmark[8].y
                    new_x = x_pos * self.screen_width
                    new_y = y_pos * self.screen_height
                    # Xóa hàng đợi cũ để tránh tích tụ
                    while self.position_queue.qsize() > 1:
                        try:
                            self.position_queue.get_nowait()
                        except queue.Empty:
                            break
                    self.position_queue.put((new_x, new_y, frame_for_pygame))
            else:
                self.hand_detected_time = None  # Reset nếu không thấy tay nữa
            

            time.sleep(0.016)  # Giới hạn 60 FPS

    def move3(self):
        current_time = pygame.time.get_ticks()
        # Nếu chưa đủ 0.75 giây từ khi phát hiện tay thì không cho điều khiển
        # Chặn điều khiển nếu chưa phát hiện tay hoặc chưa qua 0.75 giây
        if self.hand_detected_time is None or current_time - self.hand_detected_time < self.control_delay:
            return self.last_direction  # Không điều khiển, chỉ hiển thị camera
        # Kiểm tra thời gian để đồng bộ với FPS game (90 FPS ~ 11ms)
        
        if current_time - self.last_camera_update_time < 11:
            return self.last_direction  # Giữ hướng hiện tại
        self.last_camera_update_time = current_time

        direction = self.last_direction
        frame_for_pygame = None

        # Lấy tất cả dữ liệu mới từ hàng đợi
        while True:
            try:
                new_x, new_y, frame_for_pygame = self.position_queue.get_nowait()
                self.positions.append((new_x, new_y))
                if len(self.positions) > self.BUFFER_SIZE:
                    self.positions.pop(0)
            except queue.Empty:
                break

        # Nếu có dữ liệu mới, tính toán vị trí và hướng
        if self.positions:
            # Trung bình có trọng số
            weights = np.linspace(0.5, 1.0, len(self.positions))
            avg_x = sum(p[0] * w for p, w in zip(self.positions, weights)) / sum(weights)
            avg_y = sum(p[1] * w for p, w in zip(self.positions, weights)) / sum(weights)

            dx = avg_x - self.x
            dy = avg_y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            threshold = 10  # Giảm ngưỡng để nhạy hơn
            if distance > threshold:
                dx_norm = dx / distance if distance > 0 else 0
                dy_norm = dy / distance if distance > 0 else 0

                lerp_factor = 0.3  # Tăng lerp_factor để di chuyển nhanh hơn
                self.x += (avg_x - self.x) * lerp_factor
                self.y += (avg_y - self.y) * lerp_factor
                self.x = max(0, min(self.x, self.screen_width - self.width))
                self.y = max(0, min(self.y, self.screen_height - self.height))

                angle = math.atan2(dy, dx) * 180 / math.pi
                if -22.5 <= angle < 22.5:
                    direction = "right"
                elif 22.5 <= angle < 67.5:
                    direction = "right_down"
                elif 67.5 <= angle < 112.5:
                    direction = "down"
                elif 112.5 <= angle < 157.5:
                    direction = "left_down"
                elif 157.5 <= angle or angle < -157.5:
                    direction = "left"
                elif -157.5 <= angle < -112.5:
                    direction = "left_up"
                elif -112.5 <= angle < -67.5:
                    direction = "up"
                elif -67.5 <= angle < -22.5:
                    direction = "right_up"

                if direction in self.images:
                    self.image = self.images[direction]
                    self.last_direction = direction

            self.rect.topleft = (self.x, self.y)
        
        # Cập nhật camera surface nếu có khung hình mới
        if frame_for_pygame is not None:
            pygame_frame = pygame.image.frombuffer(frame_for_pygame.tobytes(), (160, 120), "RGB")
            self.camera_surface.blit(pygame_frame, (0, 0))

        return direction

    def release_camera(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()

    def get_camera_surface(self, width=160, height=120):
        return self.camera_surface

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def eat_fish(self, enemy):
        if self.sound: # Nếu sound là True thì chạy
            self.eat_sound.play()
        self.gain_xp(enemy.fish_level)
        # self.grow(enemy.fish_level)

    def dash(self):
        if not self.is_frenzy and self.can_dash:
            self.speed *= 2
            self.is_dashing = True  # Cập nhật trạng thái dash
            self.can_dash = False
            self.dash_start_time = time.time()

    def end_dash(self):
        if self.dash_start_time and time.time() - self.dash_start_time >= 0.2:
            self.speed /= 2
            self.is_dashing = False  # Kết thúc trạng thái dash
            self.dash_start_time = None
            self.start_cooldown()


    def start_cooldown(self):
        if not self.is_frenzy:
            self.dash_cooldown = time.time()  # Bắt đầu cooldown

    def update_cooldown(self):
        if self.dash_cooldown and time.time() - self.dash_cooldown >= 1.5:
            self.can_dash = True
            self.dash_cooldown = None

    def update(self):
        # Gọi trong vòng lặp chính để cập nhật cooldown
        self.update_cooldown()
        self.end_dash()  # Kiểm tra kết thúc dash
  
