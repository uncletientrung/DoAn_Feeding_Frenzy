import pygame
import sys
from settings import *
from classes.ScoreBar import ScoreBar  # Import lớp ScoreBar
from classes.main_fish import MainFish
class TopMenu:
    def __init__(self, player: MainFish, screen, list_images_fish,pos=(0, 0), width=10000, height=1000):
        self.screen = screen
        self.main_fish: MainFish = player
        self.x, self.y = pos
        self.width = width
        self.height = height
        
        # Các thông số game
        self.previous_score = -1    
        self.bonus = 0
        self.level = 1
        self.exp = 0      # Kinh nghiệm từ 0 đến 100
        self.frenzy = 0   # FRENZY từ 0 đến 100
        self.flash_state = False
        self.flash_timer = 0
        self.frenzy_completed = False
        self.score_bar = ScoreBar(list_images_fish) # truyền list_image_fish để không bị lỗi

        # Thiết lập màu sắc và font chữ
        self.WHITE = (255, 255, 255)
        self.GRAY = (50, 50, 50)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.BLUE = (0, 120, 255)
        self.font = pygame.font.SysFont("Arial", 24)




    def draw(self, player):
        """Vẽ top menu và tất cả các thành phần của nó."""
        # Vẽ các thông tin bổ sung
        # Thanh FRENZY (viền đen, nền trắng, chữ FRENZY ẩn bên dưới)
        frenzy_bar_x = self.x + 630
        frenzy_bar_y = self.y + 15
        frenzy_bar_width = 150
        frenzy_bar_height = 20

        # Vẽ viền đen
        pygame.draw.rect(self.screen, (0, 0, 0), (frenzy_bar_x, frenzy_bar_y + 14, frenzy_bar_width, frenzy_bar_height), 2)

        # Vẽ nền trắng
        pygame.draw.rect(self.screen, self.WHITE, (frenzy_bar_x + 2, frenzy_bar_y + 15, frenzy_bar_width - 4, frenzy_bar_height - 2))

        # Lấp đầy bằng màu đỏ hoặc xanh dựa trên tình hình của thanh frenzy
        if self.main_fish.is_frenzy and self.flash_state:
            color = self.BLUE
        else:
            color = self.RED 
        frenzy_fill_width = int((self.frenzy / 100) * (frenzy_bar_width - 4))  # Độ lấp đầy
        if frenzy_fill_width > 0:
            pygame.draw.rect(self.screen, color, (frenzy_bar_x + 2, frenzy_bar_y + 15, frenzy_fill_width, frenzy_bar_height - 2))

            # Hiển thị chữ trong vùng đã lấp đầy
            frenzy_text = self.font.render("FRENZY", True, self.WHITE)  # Chữ màu trắng
            text_rect = frenzy_text.get_rect(center=(frenzy_bar_x + frenzy_bar_width // 2, frenzy_bar_y + frenzy_bar_height // 0.8))
            self.screen.blit(frenzy_text, text_rect)
            visible_text_rect = pygame.Rect(frenzy_bar_x + 2, frenzy_bar_y + 2, frenzy_fill_width, frenzy_bar_height - 4)
            self.screen.set_clip(visible_text_rect)  # Chỉ vẽ trong khu vực đã lấp đầy
            self.screen.blit(frenzy_text, text_rect)
            self.screen.set_clip(None)  # Đặt lại clip

    def update_frenzy(self, new_score):
        """Cập nhật giá trị frenzy dựa trên score."""
        if not self.main_fish.is_frenzy:  # Nếu chưa ở trạng thái MAX
            if new_score != self.previous_score:  # Phát hiện sự thay đổi
                self.frenzy += min(new_score - self.previous_score, 10)  # Giới hạn tăng tối đa là 10
                self.previous_score = new_score  # Cập nhật giá trị trước đó

            # Kiểm tra nếu đạt MAX
            if self.frenzy >= 100:  # MAX giá trị
                self.frenzy = 100
                self.main_fish.is_frenzy = True  # Kích hoạt trạng thái MAX
                self.flash_timer = 5  # Bộ đếm nhấp nháy (tùy chỉnh tần suất)
        else:   # Giảm giá trị FRENZY nếu đã MAX
            self.flash_timer -= 1
            self.main_fish.speed = PLAYER_SPEED * 1.5
            if self.flash_timer <= 0:  # Điều khiển nhấp nháy
                self.flash_state = not self.flash_state  # Đổi trạng thái nhấp nháy
                self.flash_timer = 5  # Reset bộ đếm nhấp nháy

            self.frenzy -= 1  # Giảm dần giá trị frenzy
            if self.frenzy <= 0:
                self.frenzy = -10
                self.main_fish.is_frenzy = False  # Reset trạng thái MAX
                self.flash_state = False    # Dừng nhấp nháy
                self.frenzy_completed= True

            if self.frenzy_completed:
                self.previous_score = self.score_bar.score
                self.frenzy_completed = False
                self.main_fish.speed = PLAYER_SPEED