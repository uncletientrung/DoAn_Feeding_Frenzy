import pygame
import os
from settings import *
from classes import mainmenu

class SelectionScreen:
    def __init__(self, screen):
        # Gán màn hình Pygame được truyền vào để vẽ giao diện
        self.screen = screen
        
        # Khởi tạo các font chữ cho giao diện
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)  # Font cho tiêu đề chính
        self.section_font = pygame.font.SysFont("Arial", 32, bold=True)  # Font cho tiêu đề các section
        self.button_font = pygame.font.SysFont("Arial", 28)  # Font cho nút Confirm
        self.control_font = pygame.font.SysFont("Arial", 24)  # Font cho nhãn điều khiển (control labels)

        # Định nghĩa màu sắc sử dụng trong giao diện
        self.bg_color = (15, 30, 60)  # Màu nền xanh đậm tối hơn
        self.text_color = (255, 255, 255)  # Màu chữ trắng
        self.button_color = (70, 130, 180)  # Màu xanh dương cho nút Confirm
        self.button_hover_color = (100, 160, 210)  # Màu xanh sáng khi hover nút
        self.border_color = (200, 200, 200)  # Màu viền xám nhạt cho các ô
        self.selected_border_color = (255, 255, 0)  # Màu viền vàng cho ô được chọn
        self.section_bg_color = (25, 50, 90)  # Màu nền cho các section (không dùng nữa)

        # Kích thước các ô lựa chọn
        self.map_box_width = 250
        self.map_box_height = 140
        self.box_width = 200
        self.box_height = 100
        self.spacing = 40  # Khoảng cách giữa các ô trong cùng section
        self.offset_y = 90  # Dịch giao diện xuống dưới

        # Trạng thái mặc định chọn
        self.selected = {
            "map": 0,
            "control": 0,
            "character": 0
        }

        # Cấu hình các section: map, control, character
        self.sections = {
            "map": {
                "y": 70 + self.offset_y,
                "options": self.load_images(["bg11.jpg", "bg12.jpg", "bg13.jpg"], self.map_box_width, self.map_box_height)
            },
            "control": {
                "y": 270 + self.offset_y,
                "options": self.load_images(["control1.png", "control2.png", "control3.png"], self.box_width, self.box_height)
            },
            "character": {
                "y": 420 + self.offset_y,
                "options": self.load_images(["fish1.png", "fish2.png", "fish3.png"], self.box_width, self.box_height, scale_factor=1)
            },
        }

        self.title_font = pygame.font.SysFont("comicsansms", 54, bold=True)
        self.info_font = pygame.font.SysFont("comicsansms", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 36)


        # Back button
        SCALE = 0.5
        self.btn_back = mainmenu.ImageButton(10, 10, "assets/button2/Exit.png", scale=SCALE)
        # Play button
        self.btn_play = mainmenu.ImageButton(SCREEN_WIDTH - 10 - self.btn_back.rect.width, 10, "assets/button2/Play2.png", scale=SCALE)
        #BackGround
        self.background = pygame.image.load("assets/images/bgSelection1.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_images(self, filenames, width, height, scale_factor=1):
        # Hàm tải và xử lý các hình ảnh cho ô lựa chọn
        images = []
        for filename in filenames:
            path = os.path.join(IMAGE_PATH, filename)  # Đường dẫn tới file hình ảnh
            try:
                image = pygame.image.load(path)  # Tải hình ảnh
                if scale_factor != 1:
                    orig_width, orig_height = image.get_size()
                    image = pygame.transform.scale(image, (int(orig_width * scale_factor), int(orig_height * scale_factor)))
                image = pygame.transform.scale(image, (width, height))
                             
                images.append(image)
            except FileNotFoundError:
                image = pygame.Surface((width, height))
                image.fill((80, 80, 80))
                images.append(image)
        return images

    def draw_section(self, label, options, y, selected_index, box_width, box_height):
        # Hàm vẽ một section (map, control, hoặc character)
        
        # Tính toán vị trí x để căn giữa 3 ô
        start_x = (SCREEN_WIDTH - (box_width * 3 + self.spacing * 2)) // 2
        
        # Vẽ tiêu đề section
        text = self.info_font.render(label, True, (255,215, 0))  # Màu vàng
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y - 30))  # Căn giữa tiêu đề
        self.screen.blit(text, text_rect)
        
        rects = []
        for i, image in enumerate(options):
            # Tính vị trí x cho từng ô
            x = start_x + i * (box_width + self.spacing)
            rect = pygame.Rect(x, y, box_width, box_height)  # Tạo hình chữ nhật cho ô
            rects.append(rect)
            # Vẽ hình ảnh vào ô 
            self.screen.blit(image, rect)
            
            # Vẽ viền: vàng nếu ô được chọn, xám nhạt nếu không
            border_color = self.selected_border_color if i == selected_index else self.border_color
            pygame.draw.rect(self.screen, border_color, rect, 3)


        return rects  # Trả về danh sách các hình chữ nhật để xử lý click

    def handle_click(self, mouse_pos, map_rects, control_rects, char_rects):
        # Xử lý sự kiện click chuột để chọn ô
        for i, rect in enumerate(map_rects):           
            if rect.collidepoint(mouse_pos):
                self.selected["map"] = i
                return False  # Chưa nhấn Confirm, tiếp tục ở màn hình chọn
        for i, rect in enumerate(control_rects):
            if rect.collidepoint(mouse_pos):
                self.selected["control"] = i
                return False
        for i, rect in enumerate(char_rects):
            if rect.collidepoint(mouse_pos):
                self.selected["character"] = i
                return False
        if self.btn_play.draw(self.screen):
            return True  # Nhấn Confirm, thoát màn hình chọn
        return False

    def draw(self):
        # Vẽ toàn bộ giao diện màn hình chọn
        # self.screen.fill(self.bg_color)  # Tô nền xanh đậm
        self.screen.blit(self.background, (0, 0))  # Vẽ nền
        # Vẽ tiêu đề chính
        title_text = self.title_font.render("SELECT YOUR SETTINGS", True, (255, 215, 0))
        title_shadow = self.title_font.render("SELECT YOUR SETTINGS", True, (139, 0, 0, 150))
        self.screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_text.get_width()//2 + 3, 30 + 3))
        self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 30))

        # Vẽ các section và lấy danh sách hình chữ nhật
        map_rects = self.draw_section(
            "BACKGROUND", self.sections["map"]["options"],
            self.sections["map"]["y"], self.selected["map"],
            self.map_box_width, self.map_box_height
        )
        control_rects = self.draw_section(
            "CONTROL", self.sections["control"]["options"],
            self.sections["control"]["y"], self.selected["control"],
            self.box_width, self.box_height
        )
        char_rects = self.draw_section(
            "PLAYER", self.sections["character"]["options"],
            self.sections["character"]["y"], self.selected["character"],
            self.box_width, self.box_height
        )

        # Vẽ icon back ở góc trên trái
        self.btn_back.draw(self.screen)
        # Vẽ icon play ở góc trên phải
        self.btn_play.draw(self.screen)

        # Trả về các hình chữ nhật để xử lý click
        return map_rects, control_rects, char_rects

    def get_selections(self):
        # Trả về các lựa chọn đã chọn
        return {
            "map": self.selected["map"] + 1,  # Map 1, 2, 3
            "control": self.selected["control"] + 1,  # Control 1, 2, 3
            "character": self.selected["character"] + 1  # Character 1, 2, 3
        }