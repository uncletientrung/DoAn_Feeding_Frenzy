import pygame
import cv2
import numpy as np
from pygame.locals import *
from PDBCUtill import DatabaseManager
from settings import *

class FrameBXH(DatabaseManager):
    def __init__(self, x, y):
        super().__init__()  # Cho nó kế thừa connect database
        self.x = x
        self.y = y
        self.image = pygame.image.load(IMAGE_PATH + "bxh.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100))
        self.dataset = self.SelectAll()
        self.topScore = self.SelectTopScore()
        self.font = pygame.font.Font(None, 36)
        self.row_height = 40
        self.header_height = 50
        # Thiết kế đẹp hơn với màu sắc
        self.bg_color = (240, 248, 255)  # AliceBlue background
        self.header_color = (70, 130, 180)  # SteelBlue for headers
        self.text_color = (25, 25, 112)  # MidnightBlue for text
        self.line_color = (135, 206, 235)  # SkyBlue for lines
        self.highlight_color = (173, 216, 230)  # LightBlue for hover/selection
        
        # Scrollbar settings
        self.scroll_y = 0
        self.max_scroll = max(0, len(self.dataset) * self.row_height - (SCREEN_HEIGHT - 200)) 
        self.scrollbar_width = 10
        self.scrollbar_color = (100, 149, 237)
        self.scrollbar_hover_color = (65, 105, 225)  

    def draw(self, screen):
        # Vẽ nền bảng xếp hạng
        screen.blit(self.image, (self.x, self.y)) 
        start_x = self.x + 170
        start_y = self.y + 100
        
        # Draw tên tiêu đề với màu nền header
        headers = ["Name", "Level", "Score", "Play time"]
        pygame.draw.rect(screen, self.header_color, (start_x - 50, start_y - 10, 650, self.header_height))
        for i, header in enumerate(headers):
            text = self.font.render(header, True, (255, 255, 255))  # White text for contrast
            screen.blit(text, (start_x + i * 150, start_y))
        
        # Vẽ đường kẻ phân cách dưới header
        pygame.draw.line(screen, self.line_color, (start_x - 50, start_y + self.header_height - 15),
                         (start_x + 600, start_y + self.header_height - 15), 2)
        
        # Vẽ dữ liệu với scroll
        visible_rows = (SCREEN_HEIGHT - 200) // self.row_height  # Số hàng hiển thị được
        start_idx = self.scroll_y // self.row_height
        end_idx = min(start_idx + visible_rows + 1, len(self.dataset))

        for i in range(start_idx, end_idx):
            row_y = start_y + self.header_height + (i - start_idx) * self.row_height
            if row_y + self.row_height > self.y + SCREEN_HEIGHT - 100:
                break  # Không vẽ ngoài khung
            # Highlight dòng khi hover
            mouse_pos = pygame.mouse.get_pos()
            if start_x - 50 <= mouse_pos[0] <= start_x + 600 and row_y <= mouse_pos[1] <= row_y + self.row_height:
                pygame.draw.rect(screen, self.highlight_color, (start_x - 50, row_y, 650, self.row_height))
            
            # Vẽ dữ liệu từng ô
            for j, value in enumerate(self.dataset[i]):
                text = self.font.render(str(value), True, self.text_color)
                screen.blit(text, (start_x + j * 160, row_y))

        # Vẽ thanh ScoreBar
        if self.max_scroll > 0:
            scrollbar_height = (SCREEN_HEIGHT - 200) * (SCREEN_HEIGHT - 200) / (len(self.dataset) * self.row_height)
            scrollbar_y = self.y + 50 + (self.scroll_y * (SCREEN_HEIGHT - 250) / self.max_scroll)
            scrollbar_rect = pygame.Rect(self.x + SCREEN_WIDTH - 250, scrollbar_y, self.scrollbar_width, scrollbar_height)
            
            # Hover effect cho scrollbar
            if scrollbar_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, self.scrollbar_hover_color, scrollbar_rect)
                # Xử lý kéo thanh scroll
                if pygame.mouse.get_pressed()[0]:
                    self.scroll_y = max(0, min(self.max_scroll, self.scroll_y + pygame.mouse.get_rel()[1]))
            else:
                pygame.draw.rect(screen, self.scrollbar_color, scrollbar_rect)

        self.close()

    def handle_event(self, event):
        # Xử lý scroll bằng chuột
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y = max(0, min(self.max_scroll, self.scroll_y - event.y * 20))  # Cuộn 20px mỗi lần

class ImageButton:
    def __init__(self, x, y, image_path, scale=1):
        self.image = pygame.image.load(image_path).convert_alpha()
        width = int(self.image.get_width() * scale)
        height = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self, surface):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

class MainMenu:
    def __init__(self):
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 680
        
        # Khai báo trạng thái âm thanh trước
        self.sound_on = True  # Mặc định bật âm thanh
        self.music_on = True  # Mặc định bật nhạc
        
        # Kích thước chuẩn cho các nút nhỏ (trừ Play)
        SMALL_BUTTON_WIDTH = 76
        SMALL_BUTTON_HEIGHT = 51
        PLAY_BUTTON_SIZE = 200  # Kích thước cho nút Play giữ nguyên (200x200)
        BUTTON_PADDING = 20     # Khoảng cách từ biên màn hình
        BUTTON_SPACING = 10    # Khoảng cách giữa các nút nhỏ

        # Nút Exit (góc trên bên trái)
        self.top_left_btn = ImageButton(BUTTON_PADDING -17, BUTTON_PADDING -17, "assets/button2/Exit.png", 
                                       scale=SMALL_BUTTON_WIDTH / 117)  # Scale từ 117x118 về 76x51
        
        # Nút Info và Ranking (cùng góc dưới bên trái, cạnh nhau)
        info_y = self.SCREEN_HEIGHT - SMALL_BUTTON_HEIGHT - BUTTON_PADDING
        self.bottom_left_btn = ImageButton(BUTTON_PADDING-17, info_y-5, 
                                          "assets/button2/Info.png", scale=SMALL_BUTTON_WIDTH / 117)
        self.btnRanking = ImageButton(BUTTON_PADDING + SMALL_BUTTON_WIDTH + BUTTON_SPACING -20, info_y +18, 
                                     "assets/buttons/Levels.png", scale=SMALL_BUTTON_WIDTH / 117)  # Nằm cạnh nút Info
        
        # Nút Sound và Music (góc dưới bên phải, cách đều nhau)
        sound_x = self.SCREEN_WIDTH - SMALL_BUTTON_WIDTH - BUTTON_PADDING
        self.bottom_right_btn = ImageButton(sound_x +19, self.SCREEN_HEIGHT - SMALL_BUTTON_HEIGHT - BUTTON_PADDING -5, 
                                          "assets/button2/Sound-One.png" if self.sound_on else "assets/button2/Sound-None.png", 
                                          scale=SMALL_BUTTON_WIDTH / 117)
        self.bottom_right2_btn = ImageButton(sound_x - SMALL_BUTTON_WIDTH - BUTTON_SPACING +24, 
                                            self.SCREEN_HEIGHT - SMALL_BUTTON_HEIGHT - BUTTON_PADDING -5, 
                                            "assets/button2/Music-On.png" if self.music_on else "assets/button2/Music-Off.png", 
                                            scale=SMALL_BUTTON_WIDTH / 117)
        
        # Nút Play (ở trung tâm, lớn hơn một chút)
        self.play_btn_width = PLAY_BUTTON_SIZE
        self.play_btn_height = PLAY_BUTTON_SIZE  # Đảm bảo chiều cao và rộng của nút Play là như nhau
        self.play_btn = ImageButton(
            (self.SCREEN_WIDTH - self.play_btn_width) // 2, 
            (self.SCREEN_HEIGHT - self.play_btn_height) // 2, 
            "assets/button2/Play.png", 
            scale=PLAY_BUTTON_SIZE / 275  # Scale từ 275x278 về 200x200
        )
        
        # Nút Back (dùng khi ở chế độ info hoặc ranking)
        self.back_btn = ImageButton(BUTTON_PADDING, BUTTON_PADDING, "assets/buttons/Home.png", 
                                   scale=SMALL_BUTTON_WIDTH / 117)

        # Các phần còn lại giữ nguyên (video, font, text, v.v.)
        try:
            self.cap = cv2.VideoCapture("assets/images/mainmenu.mp4")
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.success, self.video_frame = self.cap.read()
        except Exception as e:
            print(f"Lỗi: {e}")
            self.video_frame = None
            self.background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.background.fill((0, 50, 100))

        try:
            self.title_font = pygame.font.Font("assets/fonts/arial.ttf", 72)
            self.info_font = pygame.font.Font("assets/fonts/DejaVuSans.ttf", 36)
            self.score_font = pygame.font.Font("assets/fonts/DejaVuSans.ttf", 36)
        except:
            self.title_font = pygame.font.SysFont("comicsansms", 72, bold=True)
            self.info_font = pygame.font.SysFont("comicsansms", 36)
            self.score_font = pygame.font.SysFont("comicsansms", 36)

        self.title_text = self.title_font.render("FISH EAT FISH", True, (255, 215, 0))
        self.title_shadow = self.title_font.render("FISH EAT FISH", True, (139, 0, 0))

        YELLOW_COLOR = (255, 215, 0)
        self.info_texts = [
            self.info_font.render("Thanh vien nhom:", True, YELLOW_COLOR),
            self.info_font.render("Nguyen Tien Trung", True, YELLOW_COLOR),
            self.info_font.render("Nguyen Minh Thuan", True, YELLOW_COLOR),
            self.info_font.render("Nguyen Phuoc Hoa Lam", True, YELLOW_COLOR),
            self.info_font.render("Phan Hoang Vu", True, YELLOW_COLOR),
            self.info_font.render("Giao vien huong dan: Ths Le Tan Long", True, YELLOW_COLOR),
            self.info_font.render("Thong tin game:", True, YELLOW_COLOR),
            self.info_font.render("Ca lon nuot ca be la mot tro choi kinh dien", True, YELLOW_COLOR),
            self.info_font.render("noi cac con ca nho hon bi cac con ca lon hon an.", True, YELLOW_COLOR),
            self.info_font.render("Nguoi choi dieu khien ca cua minh de lon manh va song sot.", True, YELLOW_COLOR)
        ]
        
        # Trạng thái bảng thông tin
        self.is_info_mode = False
        # Trạng thái bảng xếp hạng
        self.is_ranking_mode = False
        # Tạo khung bxh
        self.frameRank = FrameBXH(120, 70)
        self.top_score = self.frameRank.topScore
        self.score_text = self.score_font.render(f"Top Scored: {self.top_score}", True, YELLOW_COLOR)

    def update(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.success, self.video_frame = self.cap.read()
            if not self.success:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.success, self.video_frame = self.cap.read()
            if self.success:
                self.video_frame = cv2.resize(self.video_frame, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                self.video_frame = cv2.cvtColor(self.video_frame, cv2.COLOR_BGR2RGB)
                self.video_surface = pygame.image.frombuffer(self.video_frame.tobytes(), 
                                                             self.video_frame.shape[1::-1], "RGB")

    def draw(self, screen):
        if self.success and self.video_frame is not None:
            screen.blit(self.video_surface, (0, 0))
        else:
            screen.fill((0, 50, 100))
        
        if not self.is_info_mode:
            title_x = (self.SCREEN_WIDTH - self.title_text.get_width()) // 2
            title_y = (self.SCREEN_HEIGHT - self.play_btn_height) // 2 - 150
            screen.blit(self.title_shadow, (title_x + 5, title_y + 5))
            screen.blit(self.title_text, (title_x, title_y))
            self.top_left_btn.draw(screen)
            self.bottom_left_btn.draw(screen)
            self.bottom_right_btn.draw(screen)
            self.bottom_right2_btn.draw(screen)
            self.btnRanking.draw(screen)
            self.play_btn.draw(screen)
            score_x = (self.SCREEN_WIDTH - self.score_text.get_width()) // 2
            score_y = (self.SCREEN_HEIGHT - self.play_btn_height) // 2 + self.play_btn_height + 5
            screen.blit(self.score_text, (score_x, score_y))
        elif self.is_info_mode and not self.is_ranking_mode:
            y_offset = 100
            for text in self.info_texts:
                text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
                screen.blit(text, text_rect)
                y_offset += text.get_height() + 10
            self.back_btn.draw(screen)
        elif self.is_info_mode and self.is_ranking_mode:
            self.frameRank.draw(screen)
            self.back_btn.draw(screen)

    def update_top_score(self, new_score):
        if new_score > self.top_score:
            self.top_score = new_score
            self.score_text = self.score_font.render(f"Top Scored: {self.top_score}", True, (255, 215, 0))

                                


    def update(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.success, self.video_frame = self.cap.read()
            if not self.success:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.success, self.video_frame = self.cap.read()
            if self.success:
                self.video_frame = cv2.resize(self.video_frame, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                self.video_frame = cv2.cvtColor(self.video_frame, cv2.COLOR_BGR2RGB)
                self.video_surface = pygame.image.frombuffer(self.video_frame.tobytes(), 
                                                             self.video_frame.shape[1::-1], "RGB")

    def draw(self, screen):
        if self.success and self.video_frame is not None:
            screen.blit(self.video_surface, (0, 0))
        else:
            screen.fill((0, 50, 100))
        
        if not self.is_info_mode:
            title_x = (self.SCREEN_WIDTH - self.title_text.get_width()) // 2 + 30
            title_y = (self.SCREEN_HEIGHT - self.play_btn_height) // 2 - 150
            screen.blit(self.title_shadow, (title_x + 5, title_y + 5))
            screen.blit(self.title_text, (title_x, title_y))
            self.top_left_btn.draw(screen)
            self.bottom_left_btn.draw(screen)
            self.bottom_right_btn.draw(screen)
            self.bottom_right2_btn.draw(screen)
            self.btnRanking.draw(screen)
            self.play_btn.draw(screen)
            score_x = (self.SCREEN_WIDTH - self.score_text.get_width()) // 2 - 15
            score_y = (self.SCREEN_HEIGHT - self.play_btn_height) // 2 + 30 + self.play_btn_height + 5
            screen.blit(self.score_text, (score_x, score_y))
        elif self.is_info_mode and not self.is_ranking_mode:
            y_offset = 100
            for text in self.info_texts:
                text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, y_offset))
                screen.blit(text, text_rect)
                y_offset += text.get_height() + 10
            self.back_btn.draw(screen)
        elif self.is_info_mode and  self.is_ranking_mode:
            self.frameRank.draw(screen)
            self.back_btn.draw(screen)


    def update_top_score(self, new_score):
        if new_score > self.top_score:
            self.top_score = new_score
            self.score_text = self.score_font.render(f"Top Scored: {self.top_score}", True, (255, 215, 0))