
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
        # Tạo từ điển chứa các hình ảnh của cá theo 8 hướng
        base_size = SCREEN_WIDTH // 25

        # lấy danh sách các cá bên settings
        self.images = list_images_fish
        # kiểm tra list cá vừa lấy là list cá số mấy
        self.fish_number = self.images["fish_number"]

        # Các thuộc tính ban đầu
        base_size = SCREEN_WIDTH // 25  # Tính toán kích thước cơ bản cho cá

        # Resize tất cả 8 hướng trong từ điển self.images
        for direction in self.images:
            if direction != "fish_number":
                self.images[direction] = pygame.transform.scale(self.images[direction], (base_size, base_size))
        self.image = self.images["right"]  # Hình ảnh ban đầu (phải)
        self.x, self.y = x, y
        self.width, self.height = self.image.get_size()
        self.speed = PLAYER_SPEED
        self.score = 0
        self.size = 1
        self.size_old = 1
        self.eat_count = 0
        self.level = 9  # Mặc định level là 9 (theo yêu cầu trước)
        self.eat_sound = pygame.mixer.Sound(SOUND_PATH + "eat.wav")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.can_dash = True
        self.dash_cooldown = 1.5
        self.is_frenzy = False
        self.dash_start_time = 0
        self.data = []
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Khởi tạo Mediapipe
        self.cap = cv2.VideoCapture(0)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Giảm độ phân giải
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

        # Biến cho làm mượt di chuyển
        self.positions = []  # Danh sách lưu vị trí trung bình
        self.BUFFER_SIZE = 1  # Giảm để nhạy hơn
        self.max_speed = 8  # Tốc độ tối đa của cá (pixel/frame)

    def check_collision(self, enemies, dataScore, screen=None):  # Thêm tham số screen với giá trị mặc định None
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
                    self.data = dataScore  # gán điểm cuối khi va chạm
                    if screen:  # Nếu screen được truyền vào
                        self.game_over(screen)
                    else:
                        self.game_over()  # Gọi với giá trị mặc định
                else:
                    print(f" Cá cùng cấp, không thể ăn!")

    def grow(self, enemy_level):
        """Làm cá chính to lên khi ăn cá nhỏ hơn"""
        self.size += 0.1 * (1 + enemy_level * 0.1)  # Tăng kích thước nhanh hơn khi ăn cá lớn
        if self.size >= self.size_old + 1:
            self.size_old = int(self.size) + self.size * 0.1  # Ngưỡng lên cấp tăng dần
            self.level += 1
            pygame.mixer.Sound.play(sound_level_up)

        # Tính toán kích thước mới
        base_size = SCREEN_WIDTH // 25
        new_size = int(base_size * (1 + self.size * 0.07))  # Tỉ lệ kích thước tăng theo level
        max_size = SCREEN_WIDTH // 3  # Giới hạn kích thước tối đa
        new_size = min(new_size, max_size)

        # Resize tất cả hình ảnh theo kích thước mới
        for direction in self.images:
            if direction != "fish_number":
                self.images[direction] = pygame.transform.scale(
                    pygame.image.load(IMAGE_PATH + f"fish{self.fish_number}_{direction}.png"), (new_size, new_size)
                )
                print(f"fish{self.fish_number}_{direction}.png")

        self.width, self.height = new_size, new_size

    def move1(self, keys):
        """Di chuyển cá chính bằng phím mũi tên với hỗ trợ 8 hướng"""
        current_direction = None  # Mặc định không có hướng
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

        # Cập nhật hình ảnh cá theo hướng di chuyển
        if current_direction:
            self.image = self.images[current_direction]

        # Cập nhật vị trí hình chữ nhật đại diện cá
        self.rect.topleft = (self.x, self.y)

    def move2(self, keys):
        """Di chuyển cá chính bằng phím WASD với hỗ trợ 8 hướng"""
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
        # Cập nhật hình ảnh cá theo hướng di chuyển
        if current_direction:
            self.image = self.images[current_direction]
        # Cập nhật vị trí hình chữ nhật đại diện cá
        self.rect.topleft = (self.x, self.y)

    def move3(self):
        
        success, frame = self.cap.read()
        direction = None
        if not success:
            return None

        # Lật ảnh để giống gương
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)

        # Chuẩn bị khung hình cho camera_surface
        frame_resized = cv2.resize(frame, (160, 120))
        frame_for_pygame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Lấy vị trí đầu ngón trỏ (landmark 8)
                x_pos = hand_landmarks.landmark[8].x
                y_pos = hand_landmarks.landmark[8].y

                # Chuyển đổi sang tọa độ màn hình game
                new_x = x_pos * self.screen_width
                new_y = y_pos * self.screen_height

                # Thêm vị trí vào bộ nhớ đệm
                self.positions.append((new_x, new_y))
                if len(self.positions) > self.BUFFER_SIZE:
                    self.positions.pop(0)  # Giữ lại BUFFER_SIZE phần tử gần nhất

                # Tính trung bình để làm mượt di chuyển
                avg_x = sum(p[0] for p in self.positions) / len(self.positions)
                avg_y = sum(p[1] for p in self.positions) / len(self.positions)

                # Tính vector di chuyển
                dx = avg_x - self.x
                dy = avg_y - self.y
                distance = math.sqrt(dx**2 + dy**2)

                # Xác định hướng dựa trên dx, dy như hình vuông
                threshold = 20  # Ngưỡng thay đổi hướng (pixel)
                if distance > threshold:
                    # Chuẩn hóa vector di chuyển
                    if distance > 0:
                        dx_norm = dx / distance
                        dy_norm = dy / distance
                    else:
                        dx_norm, dy_norm = 0, 0

                    # Giới hạn tốc độ di chuyển
                    move_x = dx_norm * self.max_speed
                    move_y = dy_norm * self.max_speed

                    # Cập nhật vị trí cá
                    self.x += move_x
                    self.y += move_y
                    self.x = max(0, min(self.x, self.screen_width - self.width))
                    self.y = max(0, min(self.y, self.screen_height - self.height))

                    # Xác định hướng dựa trên dx, dy
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

                # Cập nhật rect
                self.rect.topleft = (self.x, self.y)

                # Vẽ khung xương tay lên khung hình
                frame_for_pygame = np.copy(frame_resized)  # Sao chép để vẽ khung xương
                frame_for_pygame = cv2.cvtColor(frame_for_pygame, cv2.COLOR_BGR2RGB)
                self.mp_draw.draw_landmarks(
                    frame_for_pygame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        # Cập nhật camera_surface
        pygame_frame = pygame.image.frombuffer(frame_for_pygame.tobytes(), (160, 120), "RGB")
        self.camera_surface.blit(pygame_frame, (0, 0))

        return direction

    def update_camera_frame(self):
        # Không cần hàm này nữa vì move3 đã xử lý camera_surface
        pass

    def get_camera_surface(self, width=160, height=120):
        # Trả về camera_surface trực tiếp vì đã được cập nhật trong move3
        return self.camera_surface

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def game_over(self, screen):
        self.Insert(self.data)

        pygame.mixer.Sound.play(sound_death)
        pygame.time.delay(600)
        pygame.mixer.Sound.play(sound_game_over2)

        # Tải hình ảnh bar.png từ thư mục buttons
        try:
            game_over_image = pygame.image.load("assets/buttons/bar.png")
        except FileNotFoundError:
            print(f"Không tìm thấy file bar.png trong assets/buttons!")
            pygame.quit()
            sys.exit()

        # Đặt kích thước mới cho bar.png: chỉ đủ hiển thị 3 người chơi ở trung tâm
        target_width = 400
        target_height = 300

        # Thu nhỏ hình ảnh bar.png về kích thước mới
        game_over_image = pygame.transform.scale(game_over_image, (target_width, target_height))
        game_over_rect = game_over_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Tải hai nút
        try:
            repeat_button_image = pygame.image.load("assets/button2/button_restart-sheet1.png")
            home_button_image = pygame.image.load("assets/buttons/Home.png")
        except FileNotFoundError:
            print(f"Không tìm thấy file Repeat-Right.png hoặc Home.png trong assets/buttons!")
            pygame.quit()
            sys.exit()

        # Thu nhỏ nút về kích thước phù hợp (ví dụ: 100x50)
        button_width, button_height = 100, 50
        repeat_button_image = pygame.transform.scale(repeat_button_image, (button_width, button_height))
        home_button_image = pygame.transform.scale(home_button_image, (button_width, button_height))

        # Vị trí nút dưới bar (cách bar 20 pixel)
        repeat_button_rect = repeat_button_image.get_rect(center=(SCREEN_WIDTH // 2 - 60, game_over_rect.bottom + 60))
        home_button_rect = home_button_image.get_rect(center=(SCREEN_WIDTH // 2 + 60, game_over_rect.bottom + 60))

        # Font để hiển thị text
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)

        # Giả sử có danh sách top 3 người chơi
        top_scores = [
            {"name": "Player1", "score": 1000},
            {"name": "Player2", "score": 800},
            {"name": "Player3", "score": 600}
        ]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if repeat_button_rect.collidepoint(event.pos):
                        self.restart_game()  # Restart game
                        return  # Thoát khỏi game over và quay lại game
                    if home_button_rect.collidepoint(event.pos):
                        pygame.quit()  # Hoặc quay về main menu (cần chỉnh Main.py)
                        sys.exit()

            screen.blit(game_over_image, game_over_rect)

            # Vẽ "Your Score" ở trên cùng của bảng
            your_score_text = font.render(f"Your Score: {self.score}", True, (255, 255, 255))
            your_score_rect = your_score_text.get_rect(center=(SCREEN_WIDTH // 2, game_over_rect.top - 30))
            screen.blit(your_score_text, your_score_rect)

            # Vẽ top 3 người chơi với màu khác nhau
            colors = [(0, 0, 0), (128, 0, 128), (0, 0, 255)]  # Đen, Tím, Xanh dương
            for i, player in enumerate(top_scores):
                top_text = small_font.render(f"{i+1}. {player['name']}: {player['score']}", True, colors[i])
                top_rect = top_text.get_rect(center=(SCREEN_WIDTH // 2, game_over_rect.centery + (i - 1) * 40))
                screen.blit(top_text, top_rect)

            # Vẽ hai nút
            screen.blit(repeat_button_image, repeat_button_rect)
            screen.blit(home_button_image, home_button_rect)

            pygame.display.flip()

        # Nếu thoát vòng lặp
        pygame.quit()
        sys.exit()

    def restart_game(self):
        """Reset cá chính về trạng thái ban đầu với vị trí ngẫu nhiên và level mặc định là 9"""
        # Tạo vị trí ngẫu nhiên trong màn hình, đảm bảo không nằm quá gần biên
        self.x = max(50, min(random.randint(50, SCREEN_WIDTH - 50 - self.width), SCREEN_WIDTH - 50 - self.width))
        self.y = max(50, min(random.randint(50, SCREEN_HEIGHT - 50 - self.height), SCREEN_HEIGHT - 50 - self.height))

        # Reset level về 9 (theo yêu cầu)
        self.level = 9
        self.size = 1  # Reset kích thước về mức ban đầu
        self.eat_count = 0
        self.score = 0  # Reset điểm về 0

        # Cập nhật kích thước hình ảnh về kích thước ban đầu (như trong __init__)
        base_size = SCREEN_WIDTH // 25  # Kích thước cơ bản giống lúc khởi tạo
        new_size = base_size  # Không nhân thêm hệ số, giữ nguyên kích thước ban đầu

        # Resize tất cả hình ảnh theo kích thước ban đầu
        for direction in self.images:
            if direction != "fish_number":
                self.images[direction] = pygame.transform.scale(
                    pygame.image.load(IMAGE_PATH + f"fish{self.fish_number}_{direction}.png"), (new_size, new_size)
                )

        self.width, self.height = new_size, new_size
        self.image = self.images["right"]  # Đặt lại hướng mặc định là "right"

        # Cập nhật vị trí hình chữ nhật đại diện cá
        self.rect.topleft = (self.x, self.y)

    def eat_fish(self, enemy):
        """Xử lý khi cá chính ăn cá nhỏ hơn"""
        self.eat_sound.play()
        self.grow(enemy.fish_level)
        print(f"🍽️ Đã ăn cá! Player Level: {self.level} - Enemy Level: {enemy.fish_level}")

    def dash(self):
        if not self.is_frenzy:
            if self.can_dash:
                self.speed *= 2  # Tăng tốc độ
                self.can_dash = False  # Ngăn dash tiếp
                self.dash_start_time = time.time()  # Ghi thời gian bắt đầu dash

    def end_dash(self):
        if self.dash_start_time and time.time() - self.dash_start_time >= 0.2:  # Dash kéo dài 0.05 giây
            self.speed /= 2  # Khôi phục tốc độ ban đầu
            self.dash_start_time = None  # Xóa trạng thái dash
            self.start_cooldown()  # Bắt đầu cooldown

    def start_cooldown(self):
        if not self.is_frenzy:
            if not self.dash_cooldown:  # Nếu chưa bắt đầu cooldown
                self.dash_cooldown = time.time()  # Ghi thời gian bắt đầu cooldown
            elif time.time() - self.dash_cooldown >= 1.5:  # Cooldown kéo dài 1.5 giây
                self.can_dash = True  # Cho phép dash lại
                self.dash_cooldown = None  # Kết thúc cooldown
