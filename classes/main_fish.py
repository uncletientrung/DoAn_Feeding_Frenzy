import math
import pygame
import sys
import pygame.time
from settings import *
import classes.ScoreBar

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
        self.level = 7
        self.eat_sound = pygame.mixer.Sound(SOUND_PATH + "eat.wav")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def check_collision(self, enemies):
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
                    self.game_over()
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

    def game_over(self):
        pygame.mixer.Sound.play(sound_death)
        pygame.time.delay(600)
        pygame.mixer.Sound.play(sound_game_over2)
        print("💀 Game Over! Bạn đã bị ăn!")
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    def restart_game(self):
        """Reset cá chính về trạng thái ban đầu"""
        self.x, self.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.level = 0
        self.size = 1
        self.eat_count = 0

        base_size = SCREEN_WIDTH // 25
        self.image = self.images["right"]
        self.width, self.height = base_size, base_size

    def eat_fish(self, enemy):
        """Xử lý khi cá chính ăn cá nhỏ hơn"""
        self.eat_sound.play()
        self.grow(enemy.fish_level)
        print(f"🍽️ Đã ăn cá! Player Level: {self.level} - Enemy Level: {enemy.fish_level}")

# class MainFish:
#     def __init__(self, x, y):
#         self.image_right = pygame.image.load(IMAGE_PATH + "Fishright11.png")
#         self.image_left = pygame.image.load(IMAGE_PATH + "Fishleft11.png")
        
#         #  Lưu kích thước gốc của cá
#         self.base_width, self.base_height = self.image_right.get_size()

#         #  Resize ảnh ban đầu theo màn hình
#         base_size = SCREEN_WIDTH // 25  
#         self.image_right = pygame.transform.scale(self.image_right, (base_size, base_size))
#         self.image_left = pygame.transform.scale(self.image_left, (base_size, base_size))
#         self.score=0
#         self.image = self.image_right  
#         self.x, self.y = x, y
#         self.width, self.height = self.image.get_size()
#         self.speed = PLAYER_SPEED
#         self.size = 1  
#         self.size_old=1
#         self.eat_count = 0  
#         self.level = 7  
#         self.eat_sound = pygame.mixer.Sound(SOUND_PATH + "eat.wav")
#         self.rect = self.image.get_rect(topleft=(self.x, self.y)) 

#     def check_collision(self, enemies):
#         player_mask = pygame.mask.from_surface(self.image)  

#         for enemy in enemies[:]:  
#             enemy_mask = pygame.mask.from_surface(enemy.image)  
#             enemy_offset = (enemy.x - self.x, enemy.y - self.y) 

#             if player_mask.overlap(enemy_mask, enemy_offset): 
#                 if self.level >= enemy.size:
#                     self.eat_fish(enemy)
#                     self.score+=enemy.score_enemy
#                     enemies.remove(enemy)
#                 elif self.level < enemy.size:
#                     print(f" Bạn va chạm với cá lớn hơn! Player Level: {self.level} - Enemy Level: {enemy.size}")
#                     self.game_over()
#                 else:
#                     print(f" Cá cùng cấp, không thể ăn!")


#     def grow(self, enemy_level):
#         """Làm cá chính to lên khi ăn cá nhỏ hơn"""
#         self.size += 0.1 * (1 + enemy_level * 0.1)  # Tăng kích thước nhanh hơn khi ăn cá lớn
#         if self.size>=self.size_old+1:
#             self.size_old=int(self.size)+ self.size*0.1# Ngưỡng lên cấp tăng dần
#             self.level += 1
#             pygame.mixer.Sound.play(sound_level_up)


#         # Tính toán kích thước mới
#         base_size = SCREEN_WIDTH // 25
#         new_size = int(base_size * (1 + self.size * 0.07)) #luc dau la 0.05
#         max_size = SCREEN_WIDTH // 3  # Giới hạn kích thước tối đa
#         new_size = min(new_size, max_size)

#         # Load lại hình ảnh để cập nhật kích thước
#         self.image_right = pygame.image.load(IMAGE_PATH + "fish_right.png")
#         self.image_left = pygame.image.load(IMAGE_PATH + "fish_left.png")
#         self.image_up = pygame.image.load(IMAGE_PATH + "fish_up.png")
#         self.image_right = pygame.transform.scale(self.image_right, (new_size, new_size))
#         self.image_left = pygame.transform.scale(self.image_left, (new_size, new_size))
       
#         self.width, self.height = new_size, new_size
#         global enemy_fishes 
#         enemy_fishes = [] 

#     def move1(self, keys):
#         """Di chuyển cá chính bằng phím mũi tên"""
#         if keys[pygame.K_LEFT] and self.x > 0:
#             self.x -= self.speed
#             self.image = self.image_left  # Quay trái
#         if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
#             self.x += self.speed
#             self.image = self.image_right  # Quay phải
#         if keys[pygame.K_UP] and self.y > 0:
#             self.y -= self.speed
#         if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
#             self.y += self.speed
#         self.rect.topleft = (self.x, self.y)

#     #move tich hop ai va phim
#     def move(self, dx, dy):
#         """Di chuyển cá chính bằng AI hoặc phím"""
#         if dx < 0:
#             self.image = self.image_left  # Quay trái
#         elif dx > 0:
#             self.image = self.image_right  # Quay phải

#         self.x += dx
#         self.y += dy

#         # Giới hạn phạm vi di chuyển trong màn hình
#         self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
#         self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))

#         self.rect.topleft = (self.x, self.y)

#     def draw(self, screen):
#         screen.blit(self.image, (self.x, self.y))

#     def game_over(self):
#         pygame.mixer.Sound.play(sound_death)
#         pygame.time.delay(600)
#         pygame.mixer.Sound.play(sound_game_over2)  
#         print("💀 Game Over! Bạn đã bị ăn!")
#         pygame.time.delay(3000)  
#         pygame.quit()
#         sys.exit()


#     def restart_game(self):
#         """Reset cá chính về trạng thái ban đầu"""
#         self.x, self.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
#         self.level = 0
#         self.size = 1
#         self.eat_count = 0

#         base_size = SCREEN_WIDTH // 25
#         self.image_right = pygame.image.load(IMAGE_PATH + "Fishright11.png")
#         self.image_left = pygame.image.load(IMAGE_PATH + "Fishleft11.png")
#         self.image_right = pygame.transform.scale(self.image_right, (base_size, base_size))
#         self.image_left = pygame.transform.scale(self.image_left, (base_size, base_size))
#         self.image = self.image_right  


#     def eat_fish(self, enemy):
#         """Xử lý khi cá chính ăn cá nhỏ hơn"""
#         self.eat_sound.play()

#         self.grow(enemy.fish_level) 
#         print(f"🍽️ Đã ăn cá! Player Level: {self.level} - Enemy Level: {enemy.fish_level}")
