import pygame
from settings import *
from classes.mainmenu import ImageButton,FrameBXH
SCALE = 0.6
BTN_WIDTH = int(117 * SCALE-0.1)
BTN_HEIGHT = int(118 * SCALE-0.1)
PADDING = 10

class GameOver():
    def __init__(self,screen,score,sound):
        self.screen=screen
        self.sound=sound
        self.title_font=pygame.font.SysFont("comicsansms", 80, bold=True)
        self.info_font = pygame.font.SysFont("comicsansms", 80)
        self.score_font = pygame.font.SysFont("comicsansms", 36,bold=True)
        self.image_background = pygame.image.load("assets/images/bgSelection2.png").convert()
        self.image_background = pygame.transform.scale(self.image_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.image_YourScore = pygame.image.load("assets/images/YourScore.png").convert_alpha()
        self.image_YourScore = pygame.transform.scale(self.image_YourScore,
                            (SCREEN_WIDTH//2, SCREEN_HEIGHT//5))  # Không dùng
        
        self.btn_restart = ImageButton(SCREEN_WIDTH//2-40, SCREEN_HEIGHT//2, "assets/button2/Restart.png", scale=SCALE)
        self.btn_exit= ImageButton(10, 10, "assets/button2/Exit.png", scale=SCALE)     
        self.btn_menu= ImageButton(PADDING, SCREEN_HEIGHT - BTN_HEIGHT - PADDING, "assets/button2/button_menu-sheet1.png", scale=SCALE)   

        self.score=score  # Màu vàng
        frameRank=FrameBXH(0,0) # Tạo biến Frame nhưng không draw để lấy topScrore
        self.top_score = frameRank.topScore
        

    def draw(self):
        self.screen.blit(self.image_background, (0, 0))
        # Vẽ tiêu đề "YOUR SCORE"
        title_text = self.title_font.render("YOUR SCORE", True, (255, 215, 0))
        title_shadow = self.title_font.render("YOUR SCORE", True, (139, 0, 0, 150))
        self.screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_text.get_width()//2 + 3, 30 + 3))
        self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 30))

        self.btn_restart.draw(self.screen,self.sound)
        self.btn_exit.draw(self.screen,self.sound)
        self.btn_menu.draw(self.screen,self.sound) 
        # Vẽ điểm
        score_text = self.title_font.render(f"{self.score}", True, (255, 215, 0))
        score_shadow = self.title_font.render(f"{self.score}", True, (139, 0, 0, 150))
        self.screen.blit(score_shadow, (SCREEN_WIDTH//2 - score_shadow.get_width()//2 + 3, 160+3))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2,160))
        # Vẽ điểm cao nhất
        best_score_text = self.score_font.render(f"Top Score: {self.top_score}", True, (255, 215, 0))
        best_score_shadow = self.score_font.render(f"Top Score: {self.top_score}", True, (139, 0, 0, 150))
        self.screen.blit(best_score_shadow, (SCREEN_WIDTH//2 - best_score_text.get_width()//2 + 3, 500+3))
        self.screen.blit(best_score_text, (SCREEN_WIDTH//2 - best_score_text.get_width()//2, 500))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if self.btn_restart.draw(self.screen,self.sound):
            return "restart"
        if self.btn_exit.draw(self.screen,self.sound):
            return "exit"
        if self.btn_menu.draw(self.screen,self.sound):
            return "menu"
        return True
    

