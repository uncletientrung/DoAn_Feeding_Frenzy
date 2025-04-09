import math
import pygame
import sys
import pygame.time
from settings import *
import classes.ScoreBar
import time
#ákgfbhjsdfb
class MainFish:
    def __init__(self, x, y):
        # Tạo từ điển chứa các hình ảnh của cá theo 8 hướng
        base_size = SCREEN_WIDTH // 25
        self.images = {
            "left_down": pygame.image.load(IMAGE_PATH + "fish_left_down.png"),
            "left_up": pygame.image.load(IMAGE_PATH + "fish_left_up.png"),
            "right": pygame.image.load(IMAGE_PATH + "fish_right.png"),
            "down": pygame.image.load(IMAGE_PATH + "fish_down.png"),
            "left": pygame.image.load(IMAGE_PATH + "fish_left.png"),
            "up": pygame.image.load(IMAGE_PATH + "fish_up.png"),
            "right_down": pygame.image.load(IMAGE_PATH + "fish_right_down.png"),
            "right_up": pygame.image.load(IMAGE_PATH + "fish_right_up.png")
        }

        # Các thuộc tính ban đầu
        base_size = SCREEN_WIDTH // 25  # Tính toán kích thước cơ bản cho cá

    # Resize tất cả 8 hướng trong từ điển self.images
        for direction in self.images:
            self.images[direction] = pygame.transform.scale(self.images[direction], (base_size, base_size))
        self.image = self.images["right"]  # Hình ảnh ban đầu (phải)
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

    def check_collision(self, enemies, screen=None):  # Thêm tham số screen với giá trị mặc định None
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
                    print(f" Bạn va chạm với cá lớn hơn! Player Level: {self.level} - Enemy Level: {enemy.size}")
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
            self.images[direction] = pygame.transform.scale(
                pygame.image.load(IMAGE_PATH + f"fish_{direction}.png"), (new_size, new_size)
            )

        self.width, self.height = new_size, new_size
        global enemy_fishes
        enemy_fishes = []

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

    def move(self, dx, dy):
        """Di chuyển cá chính bằng AI hoặc phím"""
        if dx < 0 and dy < 0:
            current_direction = "left_up"
        elif dx > 0 and dy < 0:
            current_direction = "right_up"
        elif dx < 0 and dy > 0:
            current_direction = "left_down"
        elif dx > 0 and dy > 0:
            current_direction = "right_down"
        elif dx < 0:
            current_direction = "left"
        elif dx > 0:
            current_direction = "right"
        elif dy < 0:
            current_direction = "up"
        else:  # dy > 0
            current_direction = "down"

        self.image = self.images[current_direction]
        self.x += dx
        self.y += dy

        # Giới hạn phạm vi di chuyển trong màn hình
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def game_over(self, screen):
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
            repeat_button_image = pygame.image.load("assets/buttons/Repeat-Right.png")
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

            # Không fill background, giữ nguyên background hiện tại
            # Vẽ hình ảnh game over đã thu nhỏ lên trung tâm
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
    """Reset cá chính về trạng thái ban đầu"""
    self.x, self.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    self.level = 0
    self.size = 1
    self.eat_count = 0
    self.score = 0

    base_size = SCREEN_WIDTH // 25
    self.image = self.images["right"]
    self.width, self.height = base_size, base_size

    def eat_fish(self, enemy):
        """Xử lý khi cá chính ăn cá nhỏ hơn"""
        self.eat_sound.play()
        self.grow(enemy.fish_level)
        print(f"🍽️ Đã ăn cá! Player Level: {self.level} - Enemy Level: {enemy.fish_level}")


