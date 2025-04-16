import pygame
import os
from settings import *
from classes import mainmenu

class SelectionScreen:
    def __init__(self, screen):
        # Gán màn hình Pygame được truyền vào để vẽ giao diện
        self.screen = screen
        
        # Khởi tạo các font chữ cho giao diện
        self.font = pygame.font.SysFont("Arial", 36)  # Font cho tiêu đề các section
        self.button_font = pygame.font.SysFont("Arial", 24)  # Font cho nút Confirm
        self.control_font = pygame.font.SysFont("Arial", 20)  # Font cho nhãn điều khiển (control labels)

        # Định nghĩa màu sắc sử dụng trong giao diện
        self.bg_color = (0, 50, 100)  # Màu nền xanh đậm, giống main menu
        self.text_color = (255, 255, 255)  # Màu chữ trắng
        self.button_color = (100, 100, 100)  # Màu xám cho nút Confirm
        self.button_hover_color = (150, 150, 150)  # Màu xám sáng khi hover nút
        self.border_color = (255, 255, 255)  # Màu viền trắng cho các ô
        self.selected_border_color = (255, 0, 0)  # Màu viền đỏ cho ô được chọn

        # Kích thước các ô lựa chọn
        self.map_box_width = 280 
        self.map_box_height = 100
        self.box_width = 220
        self.box_height = 80
        self.spacing = 80  # Khoảng cách giữa các ô trong cùng section
        self.offset_y = 30  # Dịch giao diện xuống dưới 30px để căn giữa đẹp hơn

        # Trạng thái mặc định chọn
        self.selected = {
            "map": 0,
            "control": 0,
            "character": 0
        }
        self.control_labels = ["AWDS", "Phím", "AI"]

        # Cấu hình các section: map, control, character
        self.sections = {
            "map": {
                "y": 50 + self.offset_y,  # Vị trí y của section chọn map
                "options": self.load_images(["bg11.jpg", "bg12.jpg", "bg13.jpg"], self.map_box_width, self.map_box_height)
            },
            "control": {
                "y": 250 + self.offset_y,  # Vị trí y của section chọn điều khiển
                "options": self.load_images(["control1.png", "control2.png", "control3.png"], self.box_width, self.box_height)
            },
            "character": {
                "y": 450 + self.offset_y,  # Vị trí y của section chọn nhân vật
                "options": self.load_images(["fish1.png", "fish2.png", "fish3.png"], self.box_width, self.box_height, scale_factor=0.5)
            },
        }

        # Tạo nút Confirm để xác nhận lựa chọn
        self.confirm_button_rect = pygame.Rect((SCREEN_WIDTH - 200) // 2,550 + self.offset_y,  # Đặt dưới các section
                                                                        200, 50  # Kích thước nút: 200x50
        )
        self.confirm_button_text = self.button_font.render("Confirm", True, self.text_color)  # Văn bản trên nút

        self.image_home=mainmenu.ImageButton(0,0,"assets/buttons/Exit.png")

    def load_images(self, filenames, width, height, scale_factor=1):# Hàm tải và xử lý các hình ảnh cho ô lựa chọn
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
                images.append(image)
            except FileNotFoundError:
                print(f"Không tìm thấy file {path}")
                # Nếu không tìm thấy file, tạo bề mặt màu xám làm placeholder
                image = pygame.Surface((width, height))
                image.fill((100, 100, 100))
                images.append(image)
        return images

    def draw_section(self, label, options, y, selected_index, box_width, box_height):
        # Hàm vẽ một section (map, control, hoặc character)
        # Tính toán vị trí x để căn giữa 3 ô
        start_x = (SCREEN_WIDTH - (box_width * 3 + self.spacing * 2)) // 2
        # Vẽ tiêu đề section
        text = self.font.render(label, True, self.text_color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y - 40))  # Căn giữa tiêu đề
        self.screen.blit(text, text_rect)

        rects = []
        for i, image in enumerate(options):
            # Tính vị trí x cho từng ô
            x = start_x + i * (box_width + self.spacing)
            rect = pygame.Rect(x, y, box_width, box_height)  # Tạo hình chữ nhật cho ô
            rects.append(rect)

            # Vẽ hình ảnh vào ô
            self.screen.blit(image, rect)

            # Vẽ viền: đỏ nếu ô được chọn, trắng nếu không
            border_color = self.selected_border_color if i == selected_index else self.border_color
            pygame.draw.rect(self.screen, border_color, rect, 2)

            # Nếu là section điều khiển, vẽ thêm nhãn (AWDS, Phím, AI)
            if label == "Chọn Điều khiển" and i < len(self.control_labels):
                control_text = self.control_font.render(self.control_labels[i], True, self.text_color)
                text_rect = control_text.get_rect(center=(x + box_width // 2, y + box_height // 2))
                self.screen.blit(control_text, text_rect)

        return rects  # Trả về danh sách các hình chữ nhật để xử lý click

    def handle_click(self, mouse_pos, map_rects, control_rects, char_rects):
        # Xử lý sự kiện click chuột để chọn ô
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

        # Vẽ các section và lấy danh sách hình chữ nhật
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

        # Vẽ nút Confirm
        mouse_pos = pygame.mouse.get_pos()
        # Đổi màu nút khi hover
        button_color = self.button_hover_color if self.confirm_button_rect.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, button_color, self.confirm_button_rect)
        pygame.draw.rect(self.screen, self.text_color, self.confirm_button_rect, 2)  # Vẽ viền trắng
        text_rect = self.confirm_button_text.get_rect(center=self.confirm_button_rect.center)
        self.screen.blit(self.confirm_button_text, text_rect)

        # Vẽ icon trang trí ở góc trên trái
        self.image_home.draw(self.screen)

        # Trả về các hình chữ nhật để xử lý click
        return map_rects, control_rects, char_rects

    def get_selections(self):
        # Trả về các lựa chọn đã chọn
        # Giá trị trả về là 1, 2, hoặc 3 (tương ứng với ô 0, 1, 2 + 1)
        return {
            "map": self.selected["map"] + 1,  # Map 1, 2, 3
            "control": self.selected["control"] + 1,  # Control 1, 2, 3
            "character": self.selected["character"] + 1  # Character 1, 2, 3
        }