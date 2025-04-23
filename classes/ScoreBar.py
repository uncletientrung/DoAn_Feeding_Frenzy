
import pygame
import sys
from settings import *
from classes import main_fish
import time

WHITE = (255, 255, 255)
WHITE_GLOW = (0, 255, 240)

class ScoreBar:
    def __init__(self, energy_bar_image):
        self.energy_bar_bg = energy_bar_image
        self.score = 0
        self.level = 1

        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.time_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.border_width = 2
        self.start_time = time.time()
        self.data = ["", 0, 0, ""]
        self.clock_icon = pygame.image.load("assets/images/gui_time-sheet0.png")
        self.clock_icon = pygame.transform.scale(self.clock_icon, (208, 76.7))

    def draw(self, screen, player):
        self.level = player.level
        self.score = player.score

        size = player.size
        size_old = player.size_old + 1  
        tyle_width = 1 - (size_old - size)  
        tyle_width = max(0.0, min(tyle_width, 1.0))

        current_time = time.time()
        elapsed_time = int(current_time - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        bar_x, bar_y = 10, 10
        bar_width = self.energy_bar_bg.get_width()
        bar_height = self.energy_bar_bg.get_height()
        border_thickness = 3
        avatar_width = 70
        corner_radius = 15

        # Vẽ thanh năng lượng trước
        energy_width = int((bar_width - avatar_width - border_thickness * 2) * tyle_width)
        energy_height = bar_height - border_thickness * 2
        energy_start_x = avatar_width
        energy_start_y = border_thickness

        if energy_width > 0:
            energy_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
            if energy_width >= corner_radius * 2:
                pygame.draw.rect(
                    energy_surface, WHITE_GLOW,
                    (energy_start_x, energy_start_y, energy_width, energy_height),
                    0, corner_radius, corner_radius, corner_radius, corner_radius
                )
            else:
                pygame.draw.rect(
                    energy_surface, WHITE_GLOW,
                    (energy_start_x, energy_start_y, energy_width, energy_height),
                    0, corner_radius, 0, corner_radius, corner_radius
                )
            if energy_width + energy_start_x >= bar_width - border_thickness - corner_radius:
                pygame.draw.rect(
                    energy_surface, WHITE_GLOW,
                    (bar_width - border_thickness - corner_radius, energy_start_y,
                     corner_radius, energy_height),
                    0, 0, corner_radius, 0, corner_radius
                )
            mask = pygame.mask.from_surface(self.energy_bar_bg)
            mask_surface = mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
            energy_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            screen.blit(energy_surface, (bar_x, bar_y))

        # Sau đó vẽ nền thanh năng lượng đè lên
        screen.blit(self.energy_bar_bg, (bar_x, bar_y))
        screen.blit(self.energy_bar_bg, (bar_x, bar_y), (0, 0, avatar_width, bar_height))

        # Vẽ điểm số
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, bar_y + bar_height))

        # Vẽ hình đồng hồ
        elapsed_time = time.time() - self.start_time
        seconds = int(elapsed_time)
        milliseconds = int((elapsed_time - seconds) * 100)  # chỉ lấy 2 chữ số

        # Format lại chuỗi hiển thị giây.milisec (VD: 03.42)
        time_str = f"{seconds:02d}.{milliseconds:02d}"

        # Vẽ đồng hồ
        clock_x = SCREEN_WIDTH - 220
        clock_y = bar_y
        screen.blit(self.clock_icon, (clock_x, clock_y))

        # Vẽ chuỗi thời gian vào đồng hồ
        seconds_text = self.time_font.render(time_str, True, WHITE)
        icon_w, icon_h = self.clock_icon.get_size()
        text_x = clock_x + icon_w // 2
        text_y = clock_y + (icon_h - seconds_text.get_height() - 4) // 2
        screen.blit(seconds_text, (text_x, text_y))

        # Cập nhật data
        self.data = ["Player", int(self.level), int(self.score), time_str]

    def reset_time(self):
        self.start_time = time.time()
