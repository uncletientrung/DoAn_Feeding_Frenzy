import pygame
import sys
from classes.game import Game
from classes.mainmenu import MainMenu, ImageButton
from classes.selectionScreen import SelectionScreen
from settings import *
import cv2

pygame.init()
pygame.mixer.init()
FPS = 60

class GameState:
    MENU = "menu"
    SELECTION = "selection"
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
        self.selection_screen = None
        self.game = None

    def run_menu(self):
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
                    self.menu.bottom_right_btn = ImageButton(
                        SCREEN_WIDTH-100 +24, SCREEN_HEIGHT-100 + 50, new_image_path)
                if self.menu.bottom_right2_btn.draw(self.screen):
                    self.menu.music_on = not self.menu.music_on
                    new_image_path = "assets/buttons/Music-On.png" if self.menu.music_on else "assets/buttons/Music-Off.png"
                    self.menu.bottom_right2_btn = ImageButton(
                        SCREEN_WIDTH-100-53, SCREEN_HEIGHT-100 + 50, new_image_path)
                if self.menu.bottom_left_btn.draw(self.screen):
                    self.menu.is_info_mode = True
                if self.menu.btnRanking.draw(self.screen):
                    self.menu.is_info_mode = True
                    self.menu.is_ranking_mode = True
                if self.menu.play_btn.draw(self.screen):
                    if hasattr(self.menu, 'cap') and self.menu.cap.isOpened():
                        self.menu.cap.release()
                    self.selection_screen = SelectionScreen(self.screen)
                    return GameState.SELECTION
            elif self.menu.is_info_mode and not self.menu.is_ranking_mode:
                if self.menu.back_btn.draw(self.screen):
                    self.menu.is_info_mode = False
            elif self.menu.is_info_mode and self.menu.is_ranking_mode:
                self.menu.frameRank.handle_event(event)
                if self.menu.back_btn.draw(self.screen):
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
                    self.game = Game(self.image_background, self.list_images_fish, self.choice_control)
                    return GameState.GAME
                if self.selection_screen.btn_back.draw(self.screen):
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
            self.game = Game(self.image_background, self.list_images_fish, self.choice_control)
        result = self.game.run()
        if result == "restart":
            self.game = Game(self.image_background, self.list_images_fish, self.choice_control)
            return GameState.GAME
        elif result == "menu":
            if hasattr(self.menu, 'cap') and not self.menu.cap.isOpened():
                self.menu.cap = cv2.VideoCapture("assets/images/mainmenu.mp4")
                self.menu.fps = self.menu.cap.get(cv2.CAP_PROP_FPS)
                self.menu.success, self.menu.video_frame = self.menu.cap.read()
            return GameState.MENU
        elif result == "exit":
            return GameState.EXIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.player.release_camera()
                if hasattr(self.menu, 'cap') and not self.menu.cap.isOpened():
                    self.menu.cap = cv2.VideoCapture("assets/images/mainmenu.mp4")
                    self.menu.fps = self.menu.cap.get(cv2.CAP_PROP_FPS)
                    self.menu.success, self.menu.video_frame = self.menu.cap.read()
                return GameState.MENU
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