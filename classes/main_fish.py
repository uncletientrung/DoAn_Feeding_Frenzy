import pygame
from settings import *

class MainFish:
    def __init__(self, x, y):
        self.image_right = pygame.image.load(IMAGE_PATH + "sharkleft1.png")
        self.image_left = pygame.image.load(IMAGE_PATH + "shark1.png")
        # Resize ảnh cá địch
        new_size = (SCREEN_WIDTH // 15, SCREEN_HEIGHT // 15)  
        self.image_right = pygame.transform.scale(self.image_right, new_size)
        self.image_left = pygame.transform.scale(self.image_left, new_size)
        self.image = self.image_right  
        self.x, self.y = x, y
        self.width, self.height = self.image.get_size()
        self.speed = PLAYER_SPEED
        self.size = 1  # Kích thước cá chính (tăng khi ăn)

    # def check_collision(self, enemies):
    #     for enemy in enemies:
    #         if (self.x < enemy.x + enemy.width and
    #             self.x + self.width > enemy.x and
    #             self.y < enemy.y + enemy.height and
    #             self.y + self.height > enemy.y):
                
    #             if self.size > enemy.size:  # Kiểm tra cá chính có lớn hơn không
    #                 enemy.reset_position()  # Cá địch xuất hiện lại
    #                 self.grow()

    # def grow(self):
    #     """Làm cá chính to lên"""
    #     self.size += 1
    #     self.width += 10  # Tăng kích thước lên 10px
    #     self.height += 10
    #     self.image_right = pygame.transform.scale(self.image_right, (self.width, self.height))
    #     self.image_left = pygame.transform.scale(self.image_left, (self.width, self.height))
    #     self.image = self.image_right  # Giữ hướng ban đầu


    def move(self, keys):
        """Di chuyển cá chính bằng phím mũi tên"""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.image = self.image_left  # Quay trái
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.image = self.image_right  # Quay phải
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
