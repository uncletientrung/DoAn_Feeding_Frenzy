import pygame
import os
from settings import *
from classes import mainmenu

class SelectionScreen:
    def __init__(self, screen):
        # Gán màn hình Pygame được truyền vào để vẽ giao diện
        self.screen = screen
        
        # Khởi tạo các font chữ cho giao diện (updated fonts and sizes)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)  # Font cho tiêu đề chính
        self.section_font = pygame.font.SysFont("Arial", 32, bold=True)  # Font cho tiêu đề các section
        self.button_font = pygame.font.SysFont("Arial", 28)  # Font cho nút Confirm
        self.control_font = pygame.font.SysFont("Arial", 24)  # Font cho nhãn điều khiển (control labels)

        # Định nghĩa màu sắc sử dụng trong giao diện (updated color scheme)
        self.bg_color = (15, 30, 60)  # Màu nền xanh đậm tối hơn
        self.text_color = (255, 255, 255)  # Màu chữ trắng
        self.button_color = (70, 130, 180)  # Màu xanh dương cho nút Confirm
        self.button_hover_color = (100, 160, 210)  # Màu xanh sáng khi hover nút
        self.border_color = (200, 200, 200)  # Màu viền xám nhạt cho các ô
        self.selected_border_color = (255, 215, 0)  # Màu viền vàng cho ô được chọn
        self.section_bg_color = (25, 50, 90)  # Màu nền cho các section

        # Kích thước các ô lựa chọn (updated sizes)
        self.map_box_width = 300 
        self.map_box_height = 150
        self.box_width = 240
        self.box_height = 100
        self.spacing = 40  # Khoảng cách giữa các ô trong cùng section
        self.section_padding = 30  # Padding trong mỗi section
        self.offset_y = 20  # Dịch giao diện xuống dưới

        # Trạng thái mặc định chọn
        self.selected = {
            "map": 0,
            "control": 0,
            "character": 0
        }
        self.control_labels = ["AWDS", "ARROW KEYS", "AI"]

        # Cấu hình các section: map, control, character (updated positions)
        self.sections = {
            "map": {
                "y": 120 + self.offset_y,  # Vị trí y của section chọn map
                "options": self.load_images(["bg11.jpg", "bg12.jpg", "bg13.jpg"], self.map_box_width, self.map_box_height)
            },
            "control": {
                "y": 320 + self.offset_y,  # Vị trí y của section chọn điều khiển
                "options": self.load_images(["control1.png", "control2.png", "control3.png"], self.box_width, self.box_height)
            },
            "character": {
                "y": 470 + self.offset_y,  # Vị trí y của section chọn nhân vật
                "options": self.load_images(["fish1.png", "fish2.png", "fish3.png"], self.box_width, self.box_height, scale_factor=0.5)
            },
        }

        # Tạo nút Confirm để xác nhận lựa chọn (updated position and style)
        self.confirm_button_rect = pygame.Rect((SCREEN_WIDTH - 220) // 2, 620 + self.offset_y, 220, 60)
        self.confirm_button_text = self.button_font.render("CONFIRM", True, self.text_color)

        # Back button with updated position
        self.btn_back = mainmenu.ImageButton(0, 0, "assets/buttons/Exit.png")

    def load_images(self, filenames, width, height, scale_factor=1):
        # Hàm tải và xử lý các hình ảnh cho ô lựa chọn
        images = []
        for filename in filenames:
            path = os.path.join(IMAGE_PATH, filename)  # Đường dẫn tới file hình ảnh
            try:
                image = pygame.image.load(path)  # Tải hình ảnh
                # Nếu có scale_factor khác 1, điều chỉnh kích thước trước
                if scale_factor != 1:
                    orig_width, orig_height = image.get_size()
                    image = pygame.transform.scale(image, (int(orig_width * scale_factor), int(orig_height * scale_factor)))
                # Scale lại hình ảnh để vừa với kích thước ô
                image = pygame.transform.scale(image, (width, height))
                
                # Add a subtle dark overlay to make text more readable
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 100))  # Semi-transparent black
                image.blit(overlay, (0, 0))
                
                images.append(image)
            except FileNotFoundError:
                print(f"Không tìm thấy file {path}")
                # Nếu không tìm thấy file, tạo bề mặt màu xám làm placeholder
                image = pygame.Surface((width, height))
                image.fill((80, 80, 80))
                images.append(image)
        return images

    def draw_section(self, label, options, y, selected_index, box_width, box_height):
        # Hàm vẽ một section (map, control, hoặc character)
        # Vẽ nền section với bo góc
        section_rect = pygame.Rect(
            (SCREEN_WIDTH - (box_width * 3 + self.spacing * 2 + self.section_padding * 2)) // 2,
            y - 60,
            box_width * 3 + self.spacing * 2 + self.section_padding * 2,
            box_height + self.section_padding * 2 + 40
        )
        pygame.draw.rect(self.screen, self.section_bg_color, section_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.border_color, section_rect, 2, border_radius=10)

        # Tính toán vị trí x để căn giữa 3 ô
        start_x = (SCREEN_WIDTH - (box_width * 3 + self.spacing * 2)) // 2
        
        # Vẽ tiêu đề section
        text = self.section_font.render(label, True, self.text_color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y - 30))  # Căn giữa tiêu đề
        self.screen.blit(text, text_rect)

        rects = []
        for i, image in enumerate(options):
            # Tính vị trí x cho từng ô
            x = start_x + i * (box_width + self.spacing)
            rect = pygame.Rect(x, y, box_width, box_height)  # Tạo hình chữ nhật cho ô
            rects.append(rect)

            # Vẽ hình ảnh vào ô với bo góc
            clip_rect = pygame.Rect(x, y, box_width, box_height)
            self.screen.set_clip(clip_rect)
            self.screen.blit(image, rect)
            self.screen.set_clip(None)
            
            # Vẽ viền: vàng nếu ô được chọn, xám nhạt nếu không
            border_color = self.selected_border_color if i == selected_index else self.border_color
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=8)

            # Nếu là section điều khiển, vẽ thêm nhãn (AWDS, Phím, AI)
            if label == "CONTROL" and i < len(self.control_labels):
                control_text = self.control_font.render(self.control_labels[i], True, self.text_color)
                text_rect = control_text.get_rect(center=(x + box_width // 2, y + box_height + 20))
                self.screen.blit(control_text, text_rect)

        return rects  # Trả về danh sách các hình chữ nhật để xử lý click

    def handle_click(self, mouse_pos, map_rects, control_rects, char_rects):
        # Xử lý sự kiện click chuột để chọn ô (giữ nguyên chức năng)
        # Kiểm tra click vào ô map
        for i, rect in enumerate(map_rects):
            if rect.collidepoint(mouse_pos):
                self.selected["map"] = i
                return False  # Chưa nhấn Confirm, tiếp tục ở màn hình chọn
        # Kiểm tra click vào ô điều khiển
        for i, rect in enumerate(control_rects):
            if rect.collidepoint(mouse_pos):
                self.selected["control"] = i
                return False
        # Kiểm tra click vào ô nhân vật
        for i, rect in enumerate(char_rects):
            if rect.collidepoint(mouse_pos):
                self.selected["character"] = i
                return False
        # Kiểm tra click vào nút Confirm
        if self.confirm_button_rect.collidepoint(mouse_pos):
            return True  # Nhấn Confirm, thoát màn hình chọn
        return False

    def draw(self):
        # Vẽ toàn bộ giao diện màn hình chọn
        self.screen.fill(self.bg_color)  # Tô nền xanh đậm
        
        # Vẽ tiêu đề chính
        title_text = self.title_font.render("SELECT YOUR SETTINGS", True, (255, 255, 255))
        title_shadow = self.title_font.render("SELECT YOUR SETTINGS", True, (0, 0, 0, 150))
        self.screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_text.get_width()//2 + 3, 30 + 3))
        self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 30))

        # Vẽ các section và lấy danh sách hình chữ nhật (updated labels)
        map_rects = self.draw_section(
            "MAP", self.sections["map"]["options"],
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

        # Vẽ nút Confirm với hiệu ứng hover và bo góc
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.button_hover_color if self.confirm_button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, button_color, self.confirm_button_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.text_color, self.confirm_button_rect, 2, border_radius=10)
        
        # Thêm hiệu ứng bóng cho nút
        shadow_rect = pygame.Rect(
            self.confirm_button_rect.x + 3,
            self.confirm_button_rect.y + 3,
            self.confirm_button_rect.width,
            self.confirm_button_rect.height
        )
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=10)
        
        text_rect = self.confirm_button_text.get_rect(center=self.confirm_button_rect.center)
        self.screen.blit(self.confirm_button_text, text_rect)

        # Vẽ icon back ở góc trên trái
        self.btn_back.draw(self.screen)

        # Trả về các hình chữ nhật để xử lý click
        return map_rects, control_rects, char_rects

    def get_selections(self):
        # Trả về các lựa chọn đã chọn (giữ nguyên chức năng)
        return {
            "map": self.selected["map"] + 1,  # Map 1, 2, 3
            "control": self.selected["control"] + 1,  # Control 1, 2, 3
            "character": self.selected["character"] + 1  # Character 1, 2, 3
        }