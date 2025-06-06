import pygame
import sys
from classes.game import Game
from classes.mainmenu import MainMenu, ImageButton
from classes.selectionScreen import SelectionScreen
from settings import *
from PDBCUtill import DatabaseManager
import cv2

pygame.init()
pygame.mixer.init()
FPS = 25

class GameState:
    MENU = "menu"
    SELECTION = "selection"
    GAME = "game"
    EXIT = "exit"

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fish Eat Fish")
        pygame.display.set_icon(pygame.image.load("assets/images2/game_icon-sheet0.png"))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.menu = MainMenu()
        self.selection_screen = None
        self.game = None
        self.database= DatabaseManager()
        # Chơi nhạc
        self.menu.play_music.play(-1)
        
    def update_button_image(button, image_path):
        new_image = pygame.image.load(image_path).convert_alpha()
        new_image = pygame.transform.scale(new_image, (button.rect.width, button.rect.height))
        button.image = new_image

    def run_menu(self):
        
        self.menu.update()
        self.menu.draw(self.screen) 
        # Kích thước nút
        # chỉ vẽ 1 lần ở đây — duy nhất

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if not self.menu.is_info_mode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.top_left_btn.rect.collidepoint(event.pos):
                        return GameState.EXIT

                    if self.menu.bottom_right_btn.draw(self.screen,self.menu.sound_on):
                        self.menu.sound_on = not self.menu.sound_on
                        new_image_path = "assets/button2/Sound-One.png" if self.menu.sound_on else "assets/button2/Sound-None.png"
                        new_image = pygame.image.load(new_image_path).convert_alpha()
                        width = int(new_image.get_width() * self.menu.bottom_right_btn.rect.width / new_image.get_width())
                        height = int(new_image.get_height() * self.menu.bottom_right_btn.rect.height / new_image.get_height())
                        self.menu.bottom_right_btn.image_default = pygame.image.load(new_image_path).convert_alpha()
                        self.menu.bottom_right_btn.image = pygame.transform.scale(new_image, (width, height))

                    if self.menu.bottom_right2_btn.draw(self.screen,self.menu.sound_on):
                        self.menu.music_on = not self.menu.music_on
                        new_image_path = "assets/button2/Music-On.png" if self.menu.music_on else "assets/button2/Music-Off.png"
                        new_image = pygame.image.load(new_image_path).convert_alpha()
                        width = int(new_image.get_width() * self.menu.bottom_right2_btn.rect.width / new_image.get_width())
                        height = int(new_image.get_height() * self.menu.bottom_right2_btn.rect.height / new_image.get_height())
                        self.menu.bottom_right2_btn.image_default=pygame.image.load(new_image_path).convert_alpha()
                        self.menu.bottom_right2_btn.image = pygame.transform.scale(new_image, (width, height))
                        # Tắt nhạc liền khi ấn
                        if self.menu.music_on:
                            self.menu.play_music.play(-1)
                        else:
                            self.menu.play_music.stop()

                    if self.menu.bottom_left_btn.rect.collidepoint(event.pos):
                        self.menu.is_info_mode = True

                    if self.menu.btnRanking.rect.collidepoint(event.pos):
                        self.menu.is_info_mode = True
                        self.menu.is_ranking_mode = True

                    if self.menu.play_btn.rect.collidepoint(event.pos):
                        if hasattr(self.menu, 'cap') and self.menu.cap.isOpened():
                            self.menu.cap.release()
                        self.selection_screen = SelectionScreen(self.screen,self.menu.sound_on)
                        return GameState.SELECTION

            elif self.menu.is_info_mode and not self.menu.is_ranking_mode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.back_btn.rect.collidepoint(event.pos):
                        self.menu.is_info_mode = False

            elif self.menu.is_info_mode and self.menu.is_ranking_mode:
                self.menu.frameRank.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.back_btn.rect.collidepoint(event.pos):
                        self.menu.is_info_mode = False
                        self.menu.is_ranking_mode = False

        return GameState.MENU



    def run_selection(self):
        map_rects, control_rects, char_rects = self.selection_screen.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.selection_screen.handle_click(event.pos, map_rects, control_rects, char_rects):
                    selections = self.selection_screen.get_selections()
                    self.choice_background = selections["map"]
                    self.choice_fish = selections["character"]
                    self.choice_control = selections["control"]
                    self.image_background = update_background(self.choice_background)
                    self.list_images_fish = update_images_fish(self.choice_fish)
                    self.menu.play_music.stop() # Dung nhạc khi ấn chơi trong Selection
                    self.game = Game(self.image_background, self.list_images_fish, self.choice_control,self.choice_fish,
                                    self.menu.music_on, self.menu.sound_on)
                    
                    return GameState.GAME
                if self.selection_screen.btn_back.draw(self.screen,self.menu.sound_on):
                    if hasattr(self.menu, 'cap') and not self.menu.cap.isOpened():
                        self.menu.cap = cv2.VideoCapture("assets/images/mainmenu.mp4")
                        self.menu.fps = self.menu.cap.get(cv2.CAP_PROP_FPS)
                        self.menu.success, self.menu.video_frame = self.menu.cap.read()
                    return GameState.MENU
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if hasattr(self.menu, 'cap') and not self.menu.cap.isOpened():
                    self.menu.cap = cv2.VideoCapture("assets/images/mainmenu.mp4")
                    self.menu.fps = self.menu.cap.get(cv2.CAP_PROP_FPS)
                    self.menu.success, self.menu.video_frame = self.menu.cap.read()
                return GameState.MENU
        return GameState.SELECTION
    

    def run_game(self):
        if self.game is None:
            self.game = Game(self.image_background, self.list_images_fish, self.choice_control,self.choice_fish,
                             self.menu.music_on, self.menu.sound_on)
        result,sound_bentrong,music_bentrong = self.game.run()
        # Update lại ảnh sound và music sau khi update từ bên trong ra ngoài
        self.menu.sound_on = sound_bentrong
        self.menu.music_on = music_bentrong
        # Ảnh Sound
        new_image_path = "assets/button2/Sound-One.png" if self.menu.sound_on else "assets/button2/Sound-None.png"
        new_image = pygame.image.load(new_image_path).convert_alpha()
        width = int(new_image.get_width() * self.menu.bottom_right_btn.rect.width / new_image.get_width())
        height = int(new_image.get_height() * self.menu.bottom_right_btn.rect.height / new_image.get_height())
        self.menu.bottom_right_btn.image_default = pygame.image.load(new_image_path).convert_alpha()
        self.menu.bottom_right_btn.image = pygame.transform.scale(new_image, (width, height))
        # Ảnh music
        new_image_path = "assets/button2/Music-On.png" if self.menu.music_on else "assets/button2/Music-Off.png"
        new_image = pygame.image.load(new_image_path).convert_alpha()
        width = int(new_image.get_width() * self.menu.bottom_right2_btn.rect.width / new_image.get_width())
        height = int(new_image.get_height() * self.menu.bottom_right2_btn.rect.height / new_image.get_height())
        self.menu.bottom_right2_btn.image_default=pygame.image.load(new_image_path).convert_alpha()
        self.menu.bottom_right2_btn.image = pygame.transform.scale(new_image, (width, height))

        if result == "restart":
            self.game = Game(self.image_background, self.list_images_fish, self.choice_control,self.choice_fish,
                             self.menu.music_on, self.menu.sound_on)
            return GameState.GAME
        elif result == "menu":
            self.Database = DatabaseManager()
            self.menu.frameRank.topScore=self.Database.SelectTopScore() # Cập nhật lại database
            self.menu.frameRank.dataset=self.Database.SelectAll()
            self.menu.update_top_score(self.menu.frameRank.topScore)
            
            if hasattr(self.menu, 'cap') and not self.menu.cap.isOpened():
                if self.menu.music_on:
                    self.menu.play_music.play(-1)
                else:
                    self.menu.play_music.stop()
                self.menu.cap = cv2.VideoCapture("assets/images/mainmenu.mp4")
                self.menu.fps = self.menu.cap.get(cv2.CAP_PROP_FPS)
                self.menu.success, self.menu.video_frame = self.menu.cap.read()
            return GameState.MENU
        elif result == "exit":
            return GameState.EXIT
        return GameState.GAME

    def run(self):
        while self.running:
            if self.state == GameState.MENU:
                next_state = self.run_menu()
            elif self.state == GameState.SELECTION:
                next_state = self.run_selection()
            elif self.state == GameState.GAME:
                next_state = self.run_game()

            else:
                next_state = GameState.EXIT

            if next_state == GameState.EXIT:
                self.running = False
            else:
                self.state = next_state

            pygame.display.flip()
            self.clock.tick(FPS)

        if hasattr(self.menu, 'cap') and self.menu.cap.isOpened():
            self.menu.cap.release()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main = Main()
    main.run()