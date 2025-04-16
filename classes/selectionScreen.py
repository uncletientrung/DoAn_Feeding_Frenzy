import pygame
import os
from settings import *

class SelectionScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)
        self.button_font = pygame.font.SysFont("Arial", 24)
        self.control_font = pygame.font.SysFont("Arial", 20)

        self.bg_color = (0, 50, 100)
        self.text_color = (255, 255, 255)
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)
        self.border_color = (255, 255, 255)
        self.selected_border_color = (255, 0, 0)

        self.map_box_width = 280
        self.map_box_height = 100
        self.box_width = 220
        self.box_height = 80
        self.spacing = 80
        self.offset_y = 30

        self.selected = {
            "map": 0,
            "control": 0,
            "character": 0
        }

        self.control_labels = ["AWDS", "Phím", "AI"]

        self.sections = {
            "map": {
                "y": 50 + self.offset_y,
                "options": self.load_images(["bg11.jpg", "bg12.jpg", "bg13.jpg"], self.map_box_width, self.map_box_height)
            },
            "control": {
                "y": 250 + self.offset_y,
                "options": self.load_images(["control1.png", "control2.png", "control3.png"], self.box_width, self.box_height)
            },
            "character": {
                "y": 450 + self.offset_y,
                "options": self.load_images(["fish1.png", "fish2.png", "fish3.png"], self.box_width, self.box_height, scale_factor=0.5)
            },
        }

        self.confirm_button_rect = pygame.Rect(
            (SCREEN_WIDTH - 200) // 2,
            600 + self.offset_y,
            200, 50
        )
        self.confirm_button_text = self.button_font.render("Confirm", True, self.text_color)

        try:
            self.icon_topleft = pygame.transform.scale(
                pygame.image.load(os.path.join(IMAGE_PATH, "fish_right.png")), (80, 80)
            )
        except FileNotFoundError:
            print("Không tìm thấy file icon trang trí!")
            self.icon_topleft = pygame.Surface((80, 80))

    def load_images(self, filenames, width, height, scale_factor=1):
        images = []
        for filename in filenames:
            path = os.path.join(IMAGE_PATH, filename)
            try:
                image = pygame.image.load(path)
                if scale_factor != 1:
                    orig_width, orig_height = image.get_size()
                    image = pygame.transform.scale(image, (int(orig_width * scale_factor), int(orig_height * scale_factor)))
                image = pygame.transform.scale(image, (width, height))
                images.append(image)
            except FileNotFoundError:
                print(f"Không tìm thấy file {path}")
                image = pygame.Surface((width, height))
                image.fill((100, 100, 100))
                images.append(image)
        return images

    def draw_section(self, label, options, y, selected_index, box_width, box_height):
        start_x = (SCREEN_WIDTH - (box_width * 3 + self.spacing * 2)) // 2
        text = self.font.render(label, True, self.text_color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y - 40))
        self.screen.blit(text, text_rect)

        rects = []
        for i, image in enumerate(options):
            x = start_x + i * (box_width + self.spacing)
            rect = pygame.Rect(x, y, box_width, box_height)
            rects.append(rect)
            self.screen.blit(image, rect)
            border_color = self.selected_border_color if i == selected_index else self.border_color
            pygame.draw.rect(self.screen, border_color, rect, 2)
            if label == "Chọn Điều khiển" and i < len(self.control_labels):
                control_text = self.control_font.render(self.control_labels[i], True, self.text_color)
                text_rect = control_text.get_rect(center=(x + box_width // 2, y + box_height // 2))
                self.screen.blit(control_text, text_rect)
        return rects

    def handle_click(self, mouse_pos, map_rects, control_rects, char_rects):
        for i, rect in enumerate(map_rects):
            if rect.collidepoint(mouse_pos):
                self.selected["map"] = i
                return False
        for i, rect in enumerate(control_rects):
            if rect.collidepoint(mouse_pos):
                self.selected["control"] = i
                return False
        for i, rect in enumerate(char_rects):
            if rect.collidepoint(mouse_pos):
                self.selected["character"] = i
                return False
        if self.confirm_button_rect.collidepoint(mouse_pos):
            return True
        return False

    def draw(self):
        self.screen.fill(self.bg_color)
        map_rects = self.draw_section(
            "Chọn Map", self.sections["map"]["options"],
            self.sections["map"]["y"], self.selected["map"],
            self.map_box_width, self.map_box_height
        )
        control_rects = self.draw_section(
            "Chọn Điều khiển", self.sections["control"]["options"],
            self.sections["control"]["y"], self.selected["control"],
            self.box_width, self.box_height
        )
        char_rects = self.draw_section(
            "Chọn Nhân vật", self.sections["character"]["options"],
            self.sections["character"]["y"], self.selected["character"],
            self.box_width, self.box_height
        )
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.button_hover_color if self.confirm_button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, button_color, self.confirm_button_rect)
        pygame.draw.rect(self.screen, self.text_color, self.confirm_button_rect, 2)
        text_rect = self.confirm_button_text.get_rect(center=self.confirm_button_rect.center)
        self.screen.blit(self.confirm_button_text, text_rect)
        self.screen.blit(self.icon_topleft, (10, 10))
        return map_rects, control_rects, char_rects

    def get_selections(self):
        return {
            "map": self.selected["map"] + 1,
            "control": self.selected["control"] + 1,
            "character": self.selected["character"] + 1
        }