import cv2

def rotate_image(image, angle):
    """Xoay ảnh theo góc chỉ định."""
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # Tạo ma trận xoay và áp dụng
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
    return rotated_image

# Đọc ảnh từ file
image_path = "your_image.jpg"  # Thay bằng đường dẫn ảnh của bạn
image = cv2.imread(image_path)

# Danh sách các góc xoay và tên tệp cố định để lưu
angle_name_pairs = [
    (0, "_up.jpg"),
    (90, "_right.jpg"),
    (180, "_down.jpg"),
    (270, "_left.jpg"),
    (45, "_top_right.jpg"),
    (135, "_bottom_right.jpg"),
    (225, "_bottom_left.jpg"),
    (315, "_top_left.jpg"),
]

# Xoay ảnh theo từng góc và lưu vào tệp cố định
for angle, filename in angle_name_pairs:
    rotated = rotate_image(image, angle)
    cv2.imwrite(filename, rotated)
    print(f"Đã lưu ảnh xoay {angle} độ vào tệp: {filename}")

print("Hoàn tất xoay và lưu ảnh!")