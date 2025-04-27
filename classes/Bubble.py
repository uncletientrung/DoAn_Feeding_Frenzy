import random
import pygame

class Bubble:
    def __init__(self, image, screen_width, screen_height):
        self.original_image = image
        self.scale = random.uniform(0.3, 1.0)
        self.image = pygame.transform.rotozoom(self.original_image, 0, self.scale)

        self.x = random.randint(0, screen_width - self.image.get_width())
        self.y = screen_height + random.randint(0, 100)  # bắt đầu bên dưới màn hình
        self.speed = random.uniform(1.0, 2.5)

    def update(self):
        self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self): # Kiểm tra out khỏi screen
        return self.y + self.image.get_height() < 0


