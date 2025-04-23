# import pygame
# import sys
# from settings import *
# from classes import main_fish
# import time  # Thêm import time để lấy thời gian

# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)  # Màu đỏ đậm, không trong suốt

# class ScoreBar:
#     def __init__(self, energy_bar_image):
#         self.energy_bar_bg = energy_bar_image
#         self.score = 0
#         self.level = 1

#         self.font = pygame.font.SysFont("Arial", 24, bold=True)  # Thêm chữ đậm cho rõ
#         self.border_width = 2  # Độ dày viền
#         self.start_time = time.time()  # Lưu thời gian bắt đầu (giây)
#         self.data=["",0,0,""] # khởi tạo để thêm dữ liệu vào database

#         # Kiểm tra cá số mấy để làm hình avatar
#         # self.image = list_images_fish["right"]
#         # self.image = pygame.transform.scale(self.image, (50, 50))

#     def draw(self, screen, player):
#         self.level = player.level
#         self.score = player.score
#         size = player.size
#         size_old = player.size_old + 1
#         tyle_width = 1 - (size_old - size)  # Tìm tỉ lệ chiếm bao nhiêu phần trên thanh
        
#         # Tính thời gian đã chơi (giây)
#         current_time = time.time()
#         elapsed_time = int(current_time - self.start_time)  # Thời gian trôi qua, làm tròn xuống
        
#         # Chuyển đổi thời gian thành định dạng phút:giây
#         minutes = elapsed_time // 60
#         seconds = elapsed_time % 60
#         time_str = f"Time: {minutes:02d}:{seconds:02d}"  # Định dạng 00:00       
#         # Vẽ vòng tròn bao quanh hình con cá
#         # pygame.draw.circle(screen, BLACK, (40, 40), 30, 2)
#         # # Vẽ hình con cá trong vòng tròn
#         # screen.blit(self.image, (15, 15))
#         # Thanh năng lượng
#         bar_width = 150
#         bar_height = 20
#         bar_x, bar_y = 80, 30
        
#         # Tính toán phần bên trong (không bao gồm viền)
#         inner_width = bar_width - 2 * self.border_width
#         inner_height = bar_height - 2 * self.border_width
#         inner_x = bar_x + self.border_width
#         inner_y = bar_y + self.border_width
        
#         # #
#         # pygame.draw.rect(screen, WHITE, (inner_x, inner_y, inner_width, inner_height))
        
#         # #Vẽ viền đen xung quanh
#         # pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), self.border_width)
        
#         # #Vẽ phần progress (đảm bảo không vượt quá phần bên trong)
#         # progress_width = inner_width * tyle_width
#         # pygame.draw.rect(screen, RED, (inner_x, inner_y, progress_width, inner_height))
        
#         # Hiển thị chữ "Level:" phía trên thanh năng lượng
#         level_text = self.font.render(f"Level: {self.level}", True,WHITE)
#         screen.blit(level_text, (10, 90)) 
#         score_text = self.font.render(f"Score: {self.score}", True, WHITE)
#         screen.blit(score_text, (SCREEN_WIDTH-118, 30))
#         # Hiển thị thời gian chơi phía dưới "Score"
#         time_text = self.font.render(time_str, True, WHITE)
#         screen.blit(time_text, (SCREEN_WIDTH-120, inner_y-25))  # Đặt dưới Score, cách 24 pixel (khoảng cách giữa các dòng)
#         # tạo các giá trị của data trước khi thêm vào bên gameOver 
#         self.data=["Player",int(self.level),int(self.score),time_str[6:]]

#     def reset_time(self):
#         self.start_time = time.time()
import pygame
import sys
from settings import *
from classes import main_fish
import time

WHITE = (255, 255, 255)
RED = (255, 0, 0, 160)  # Màu đỏ có alpha

class ScoreBar:
    def __init__(self, energy_bar_image):
        self.energy_bar_bg = energy_bar_image
        self.score = 0
        self.level = 1

        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.border_width = 2
        self.start_time = time.time()
        self.data = ["", 0, 0, ""]

    def draw(self, screen, player):
        self.level = player.level
        self.score = player.score

        size = player.size
        size_old = player.size_old + 1  
        tyle_width = 1 - (size_old - size)  
        tyle_width = max(0.0, min(tyle_width, 1.0))

        # Thời gian chơi
        current_time = time.time()
        elapsed_time = int(current_time - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_str = f"Time: {minutes:02d}:{seconds:02d}"

        # ===== VẼ THANH NĂNG LƯỢNG DẠNG BO TRÒN =====
        bar_x, bar_y = 10, 10
        bar_width = self.energy_bar_bg.get_width()
        bar_height = self.energy_bar_bg.get_height()
        
        # Giá trị này cần điều chỉnh dựa trên kích thước chính xác của viền
        border_thickness = 3  # Độ dày của viền trắng
        avatar_width = 70     # Chiều rộng khu vực avatar cá
        corner_radius = 15    # Bán kính bo góc
        
        # Tạo bản sao của thanh năng lượng
        bar_with_energy = self.energy_bar_bg.copy()
        
        # Tính toán kích thước và vị trí của thanh năng lượng
        energy_start_x = avatar_width 
        energy_start_y = border_thickness
        energy_width = int((bar_width - avatar_width - border_thickness * 2) * tyle_width)
        energy_height = bar_height - border_thickness * 2
        
        if energy_width > 0:
            energy_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)

            # === Mặc định: bo góc bên trái luôn luôn ===
            if energy_width >= corner_radius * 2:
                # Nếu đủ dài để bo cả hai đầu
                pygame.draw.rect(
                    energy_surface, RED,
                    (energy_start_x, energy_start_y,
                    energy_width, energy_height),
                    0, corner_radius, corner_radius, corner_radius, corner_radius
                )
            else:
                # Nếu ngắn quá, chỉ bo đầu trái thôi
                pygame.draw.rect(
                    energy_surface, RED,
                    (energy_start_x, energy_start_y,
                    energy_width, energy_height),
                    0, corner_radius, 0, corner_radius, corner_radius
                )

            # === Nếu gần đầy thì bo thêm góc phải ===
            if energy_width + energy_start_x >= bar_width - border_thickness - corner_radius:
                pygame.draw.rect(
                    energy_surface, RED,
                    (bar_width - border_thickness - corner_radius, energy_start_y,
                    corner_radius, energy_height),
                    0, 0, corner_radius, 0, corner_radius
                )

            # Áp dụng mask để giữ hình dáng khung gốc
            mask = pygame.mask.from_surface(self.energy_bar_bg)
            mask_surface = mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
            energy_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            # Vẽ năng lượng lên thanh nền
            bar_with_energy.blit(energy_surface, (0, 0))


        # Vẽ lên màn hình
        screen.blit(bar_with_energy, (bar_x, bar_y))

        # ===== THÔNG TIN KHÁC =====
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (10, bar_y + bar_height + 10))

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 118, bar_y + 20))

        time_text = self.font.render(time_str, True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 120, bar_y + 50))

        # Lưu dữ liệu cho gameOver
        self.data = ["Player", int(self.level), int(self.score), time_str[6:]]

    def reset_time(self):
        self.start_time = time.time()
