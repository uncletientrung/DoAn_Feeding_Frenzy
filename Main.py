import pygame
import sys
from classes.game import Game
from classes.mainmenu import MainMenu,ImageButton  # Import class MainMenu từ file MainMenu.py
from settings import *

# Khởi tạo Pygame một lần duy nhất
pygame.init()
pygame.mixer.init()

FPS = 60

class GameState:
    MENU = "menu"
    GAME = "game"
    EXIT = "exit"

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fish Eat Fish")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.menu = MainMenu()
        self.game = None

    def run_menu(self): #Chạy menu và up
        self.menu.update()
        self.menu.draw(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if not self.menu.is_info_mode:
                if self.menu.top_left_btn.draw(self.screen):
                    return GameState.EXIT
                if self.menu.bottom_right_btn.draw(self.screen):
                    self.menu.sound_on = not self.menu.sound_on
                    new_image_path = "assets/buttons/Sound-Two.png" if self.menu.sound_on else "assets/buttons/Sound-None.png"
                    self.menu.bottom_right_btn = ImageButton(SCREEN_WIDTH-100 +24, SCREEN_HEIGHT-100 + 50, new_image_path)
                if self.menu.bottom_right2_btn.draw(self.screen):
                    self.menu.music_on = not self.menu.music_on
                    new_image_path = "assets/buttons/Music-On.png" if self.menu.music_on else "assets/buttons/Music-Off.png"
                    self.menu.bottom_right2_btn = ImageButton(SCREEN_WIDTH-100-53, SCREEN_HEIGHT-100 + 50, new_image_path)
                if self.menu.bottom_left_btn.draw(self.screen):
                    self.menu.is_info_mode = True
                if self.menu.btnRanking.draw(self.screen):
                    self.menu.is_info_mode=True
                    self.menu.is_ranking_mode=True
                if self.menu.play_btn.draw(self.screen):
                    if hasattr(self.menu, 'cap') and self.menu.cap.isOpened():
                        self.menu.cap.release()
                    return GameState.GAME
            elif self.menu.is_info_mode and not self.menu.is_ranking_mode:
                if self.menu.back_btn.draw(self.screen):
                    self.menu.is_info_mode = False
            elif self.menu.is_info_mode and self.menu.is_ranking_mode: # ấn vào btnRanking thì sẽ chuyển 2 cái mode=True
                if self.menu.back_btn.draw(self.screen): # nếu ấn Back sẽ trả về False
                    self.menu.is_info_mode = False 
                    self.menu.is_ranking_mode=False
            
            
        return GameState.MENU

    def run_game(self):
        """Chạy Game và trả về trạng thái tiếp theo"""
        if self.game is None:
            self.game = Game()
        self.game.update()
        self.game.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return GameState.MENU
        return GameState.GAME

    def run(self):
        while self.running:
            if self.state == GameState.MENU:
                next_state = self.run_menu()
                if next_state == GameState.GAME:
                    self.state = GameState.GAME
                elif next_state == GameState.EXIT:
                    self.running = False
            elif self.state == GameState.GAME:
                next_state = self.run_game()
                if next_state == GameState.MENU:
                    self.state = GameState.MENU
                    self.menu.update_top_score(self.game.player.eat_count)
                    self.game = None
                elif next_state == GameState.EXIT:
                    self.running = False

            pygame.display.flip()
            self.clock.tick(FPS)

        if hasattr(self.menu, 'cap') and self.menu.cap.isOpened():
            self.menu.cap.release()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main = Main()
    main.run()