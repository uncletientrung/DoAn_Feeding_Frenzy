from PIL import Image

def create_solid_wood_color(width, height, color):
    # Tạo ảnh với màu gỗ trơn
    img = Image.new("RGB", (width, height), color=color)
    return img

# Kích thước hình nền
width, height = 800, 600
# Màu gỗ trơn (RGB: nâu sáng)
wood_color = (205, 133, 63)

# Tạo và lưu hình nền
solid_wood_image = create_solid_wood_color(width, height, wood_color)
solid_wood_image.save("D:\Downloads\solid_wood_texture.png")
solid_wood_image.show()  # Hiển thị hình ảnh