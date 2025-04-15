
import pygame
import random
from random import choice
from PIL import Image, ImageSequence
from settings import *

# Load GIF một lần và resize
def load_gif(path, size):
    image = Image.open(path)
    return [pygame.image.fromstring(frame.convert("RGBA").resize(size).tobytes(), size, "RGBA")
            for frame in ImageSequence.Iterator(image)]

class BossFish:
    # Tải các frame từ file GIF giống code dưới
    frames_right = load_gif(IMAGE_PATH + "shark.gif", (SCREEN_WIDTH // 12 + 150, SCREEN_WIDTH // 12 + 50))
    frames_left = load_gif(IMAGE_PATH + "sharkleft.gif", (SCREEN_WIDTH // 12 + 150, SCREEN_WIDTH // 12 + 50))

    spawn_probability = 0.01  # Xác suất xuất hiện: 1%

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames_index = 0
        self.speed = choice([-5, 5])  # Random speed
        self.warning_time = 180  # Thời gian hiển thị cảnh báo (3 giây)
        self.is_warning = True   # Cờ để hiển thị cảnh báo
        self.image = None
        self.right_frames = BossFish.frames_right
        self.left_frames = BossFish.frames_left

        # Chọn vị trí xuất hiện dựa theo hướng di chuyển
        if self.speed > 0:
            self.x = -self.right_frames[0].get_width()
        else:
            self.x = SCREEN_WIDTH

    def move_boss(self):
        if self.warning_time > 0:
            self.warning_time -= 1
        else:
            self.is_warning = False
            self.x += self.speed

        # Cập nhật frame dựa trên hướng di chuyển
        if self.speed > 0:
            self.frames_index = (self.frames_index + 1) % len(self.right_frames)
            self.image = self.right_frames[self.frames_index]
        else:
            self.frames_index = (self.frames_index + 1) % len(self.left_frames)
            self.image = self.left_frames[self.frames_index]

    def check_collision_mainfish(self, player):
        if self.is_warning:  # Không va chạm khi đang trong giai đoạn cảnh báo
            return False
        if self.speed > 0:
            boss_mask = pygame.mask.from_surface(self.right_frames[self.frames_index].convert_alpha())
        else:
            boss_mask = pygame.mask.from_surface(self.left_frames[self.frames_index].convert_alpha())
        player_mask = pygame.mask.from_surface(player.image.convert_alpha())
        player_offset = (int(player.x - self.x), int(player.y - self.y))
        return boss_mask.overlap(player_mask, player_offset) is not None

    def check_colistion_enemy(self, enemies):
        if self.is_warning:  # Không va chạm khi đang trong giai đoạn cảnh báo
            return
        if self.speed > 0:
            boss_mask = pygame.mask.from_surface(self.right_frames[self.frames_index].convert_alpha())
        else:
            boss_mask = pygame.mask.from_surface(self.left_frames[self.frames_index].convert_alpha())
        for enemy in enemies[:]:
            enemy_mask = pygame.mask.from_surface(enemy.image)
            enemy_offset = (int(enemy.x - self.x), int(enemy.y - self.y))
            if boss_mask.overlap(enemy_mask, enemy_offset):
                enemies.remove(enemy)

    def draw(self, screen):
        if self.is_warning:
            font = pygame.font.Font(None, 74)
            warning_text = font.render("!", True, (255, 0, 0))
            warning_position = (50, self.y) if self.speed > 0 else (SCREEN_WIDTH - 100, self.y)
            screen.blit(warning_text, warning_position)
        else:
            screen.blit(self.image, (self.x, self.y))

    def remove_boss(self):
        if self.speed > 0:
            return self.x > SCREEN_WIDTH  # Xóa khi góc trái vượt rìa phải
        else:
            return self.x < -self.left_frames[0].get_width()  # Xóa khi toàn bộ cá ra khỏi rìa trái

    @staticmethod
    def should_spawn():
        return random.random() < BossFish.spawn_probability