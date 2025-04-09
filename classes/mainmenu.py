import pygame
import cv2
import numpy as np
from pygame.locals import *
from PDBCUtill import DatabaseManager
from settings import *

class FrameBXH(DatabaseManager):
    def __init__(self,x,y):
        super().__init__() # Cho nó kế thừa connect database
        self.x=x
        self.y=y
        self.image=pygame.image.load(IMAGE_PATH+"bxh.png")
        self.image=pygame.transform.scale(self.image,(SCREEN_WIDTH-200,SCREEN_HEIGHT-100))
        self.dataset=self.SelectAll()
        self.topScore=self.SelectTopScore()
        self.font = pygame.font.Font(None, 36)
        self.row_height = 40
        self.header_height = 50

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
        start_x = self.x + 170
        start_y = self.y + 100  
        # Draw tên tiêu đề
        headers = ["Name", "Level", "Score", "Play time"]
        for i, header in enumerate(headers):
            text = self.font.render(header, True, (0, 0, 0))
            screen.blit(text, (start_x + i * 150, start_y))   
        pygame.draw.line(screen, (0, 0, 0), (start_x-50, start_y + self.header_height -15),
                         (start_x + 600, start_y + self.header_height- 15), 2)
        # Draw dữ liệu
        for i, row in enumerate(self.dataset):
            for j, value in enumerate(row):
                text = self.font.render(str(value), True, (0, 0, 0))
                screen.blit(text, (start_x + j * 160, start_y + self.header_height + i * self.row_height))
        self.close()

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
        # Nút Exit
        self.top_left_btn = ImageButton(0, 0, "assets/buttons/Exit.png")
        # Nút Info
        self.bottom_left_btn = ImageButton(0, self.SCREEN_HEIGHT-100 + 50, "assets/buttons/Info.png")
        # Nút BXH
        self.btnRanking=ImageButton(77,self.SCREEN_HEIGHT-100 + 50,"assets/buttons/Levels.png")
        # Trạng thái âm thanh
        self.sound_on = True
        self.music_on = True
        # Nút Sound 
        self.bottom_right_btn = ImageButton(self.SCREEN_WIDTH-100 +24, self.SCREEN_HEIGHT-100 + 50, 
                                            "assets/buttons/Sound-Two.png" if self.sound_on else "assets/buttons/Sound-None.png")
        # Nút Music
        self.bottom_right2_btn = ImageButton(self.SCREEN_WIDTH-100-53, self.SCREEN_HEIGHT-100 + 50, 
                                             "assets/buttons/Music-Off.png" if not self.music_on else "assets/buttons/Music-On.png")
        
        self.play_btn_width = 200
        self.play_btn_height = 200
        # Nút Play
        self.play_btn = ImageButton(
            (self.SCREEN_WIDTH - self.play_btn_width) // 2 + 30, 
            (self.SCREEN_HEIGHT - self.play_btn_height) // 2 + 30, 
            "assets/buttons/Play.png", 
            scale=1.5
        )
        # Nút back
        self.back_btn = ImageButton(0, 0, "assets/buttons/Home.png", scale=1.0)

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
        self.is_ranking_mode=False
        # Tạo khung bxh
        self.frameRank=FrameBXH(120,70)
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