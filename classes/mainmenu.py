import pygame
import sys
import cv2
import numpy as np
from pygame.locals import *

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 680
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish Eat Fish - Main Menu")

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
        self.top_left_btn = ImageButton(0, 0, "assets/buttons/Exit.png")
        self.bottom_left_btn = ImageButton(0, SCREEN_HEIGHT-100 + 50, "assets/buttons/Info.png")  

        self.sound_on = True  # Ban đầu âm thanh bật
        self.music_on = True  

        self.bottom_right_btn = ImageButton(SCREEN_WIDTH-100 +24, SCREEN_HEIGHT-100 + 50, 
                                          "assets/buttons/Sound-Two.png" if self.sound_on else "assets/buttons/Sound-None.png")
        self.bottom_right2_btn = ImageButton(SCREEN_WIDTH-100-53, SCREEN_HEIGHT-100 + 50, 
                                           "assets/buttons/Music-Off.png" if not self.music_on else "assets/buttons/Music-On.png")
        
        self.play_btn_width = 200
        self.play_btn_height = 200
        self.play_btn = ImageButton(
            (SCREEN_WIDTH - self.play_btn_width) // 2 +30, 
            (SCREEN_HEIGHT - self.play_btn_height) //2 + 30, 
            "assets/buttons/Play.png", 
            scale=1.5
        )

        self.back_btn = ImageButton(0, 0, "assets/buttons/Home.png", scale=1.0)

        try:
            self.cap = cv2.VideoCapture("assets/images/mainmenu.mp4")
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = self.frame_count / self.fps
            self.restart_time = pygame.time.get_ticks() + int(self.duration * 1000)
            self.success, self.video_frame = self.cap.read()
        except Exception as e:
            print(f"Lỗi: {e}")
            self.video_frame = None
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((0, 50, 100))

        try:
            self.title_font = pygame.font.Font("assets/fonts/arial.ttf", 72)
            self.info_font = pygame.font.Font("assets/fonts/DejaVuSans.ttf", 36)
            self.score_font = pygame.font.Font("assets/fonts/DejaVuSans.ttf", 36)  # Font cho điểm số
        except:
            self.title_font = pygame.font.SysFont("comicsansms", 72, bold=True)
            self.info_font = pygame.font.SysFont("comicsansms", 36)
            self.score_font = pygame.font.SysFont("comicsansms", 36)

        self.title_text = self.title_font.render("FISH EAT FISH", True, (255, 215, 0))
        self.title_shadow = self.title_font.render("FISH EAT FISH", True, (139, 0, 0))

        YELLOW_COLOR = (255, 215, 0)  # Màu vàng

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
        
        # Khởi tạo top score ban đầu là 0
        self.top_score = 0
        
        # Tạo văn bản cho top score
        self.score_text = self.score_font.render(f"Top Scored: {self.top_score}", True, YELLOW_COLOR)
        
        self.is_info_mode = False
        
        self.clock = pygame.time.Clock()
        self.running = True
#fix
    def run(self):
        while self.running:
            self.update()
            self.draw()
            self.handle_events()

        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if hasattr(self, 'cap') and self.cap is not None:
            self.success, self.video_frame = self.cap.read()
            if not self.success:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.success, self.video_frame = self.cap.read()
        
        if self.success and self.video_frame is not None:
            try:
                self.video_frame = cv2.resize(self.video_frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.video_frame = cv2.cvtColor(self.video_frame, cv2.COLOR_BGR2RGB)
                self.video_surface = pygame.image.frombuffer(self.video_frame.tobytes(), 
                                                         self.video_frame.shape[1::-1], "RGB")
            except Exception as e:
                print(f"Lỗi khi xử lý video: {e}")
                self.video_frame = None

    def draw(self):
        if self.video_frame is not None and self.success:
            screen.blit(self.video_surface, (0, 0))
        else:
            screen.fill((0, 50, 100))

        if not self.is_info_mode:  # Giao diện Main Menu
            title_x = (SCREEN_WIDTH - self.title_text.get_width()) // 2 + 30
            title_y = (SCREEN_HEIGHT - self.play_btn_height) // 2 - 150
            
            screen.blit(self.title_shadow, (title_x + 5, title_y + 5))
            screen.blit(self.title_text, (title_x, title_y))
            
            self.top_left_btn.draw(screen)
            self.bottom_left_btn.draw(screen)
            self.bottom_right_btn.draw(screen)
            self.bottom_right2_btn.draw(screen)
            self.play_btn.draw(screen)

            # Vẽ dòng "Top Scored" ngay dưới nút Play
            score_x = (SCREEN_WIDTH - self.score_text.get_width()) // 2 -15  # Căn giữa theo nút Play
            score_y = (SCREEN_HEIGHT - self.play_btn_height) // 2 + 30 + self.play_btn_height + 5  # Dưới nút Play 10 pixel
            screen.blit(self.score_text, (score_x, score_y))
        else:  # Giao diện Info
            y_offset = 100
            for text in self.info_texts:
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(text, text_rect)
                y_offset += text.get_height() + 10
            
            self.back_btn.draw(screen)

        pygame.display.flip()
        self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            
            if not self.is_info_mode:  # Xử lý sự kiện ở Main Menu
                if self.top_left_btn.draw(screen):
                    print("Exit button clicked")
                    self.running = False
                
                if self.bottom_right_btn.draw(screen):
                    print("Sound button clicked")
                    self.sound_on = not self.sound_on
                    new_image_path = "assets/buttons/Sound-Two.png" if self.sound_on else "assets/buttons/Sound-None.png"
                    self.bottom_right_btn = ImageButton(SCREEN_WIDTH-100 +24, SCREEN_HEIGHT-100 + 50, new_image_path)

                if self.bottom_right2_btn.draw(screen):
                    print("Music button clicked")
                    self.music_on = not self.music_on
                    new_image_path = "assets/buttons/Music-On.png" if self.music_on else "assets/buttons/Music-Off.png"
                    self.bottom_right2_btn = ImageButton(SCREEN_WIDTH-100-53, SCREEN_HEIGHT-100 + 50, new_image_path)
                
                if self.bottom_left_btn.draw(screen):
                    print("Info button clicked")
                    self.is_info_mode = True  # Chuyển sang chế độ Info
                
                if self.play_btn.draw(screen):
                    print("Play button clicked")
                    if hasattr(self, 'cap') and self.cap is not None:
                        self.cap.release()
                    pygame.quit()
                    import subprocess
                    subprocess.Popen([sys.executable, "Main.py"])
                    sys.exit()
            else:  # Xử lý sự kiện ở chế độ Info
                if self.back_btn.draw(screen):
                    print("Back button clicked")
                    self.is_info_mode = False  

    def update_top_score(self, new_score):
        if new_score > self.top_score:
            self.top_score = new_score
            self.score_text = self.score_font.render(f"Top Scored: {self.top_score}", True, (255, 215, 0))

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()