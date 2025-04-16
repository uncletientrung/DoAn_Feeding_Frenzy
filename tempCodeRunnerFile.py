import cv2

def rotate_image(image, angle):
    """Xoay ảnh theo góc chỉ định."""
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # Tạo ma trận xoay và áp dụng
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
    return rotated_image

def flip_image(image):
    """Lật ảnh theo chiều ngang."""
    return cv2.flip(image, 1)

# Đọc ảnh từ file
image_path = "D:\WorkSpace\DoAn_Feeding_Frenzy\assets\images\fish1.png"  # Thay bằng đường dẫn ảnh của bạn
image = cv2.imread(image_path)

# Xoay ảnh ban đầu (hướng trái)
angle_name_pairs_left = [
    (90, "image_up.jpg"),
    (45, "image_top_left.jpg"),
    (0, "image_left.jpg"),
    (315, "image_bottom_left.jpg"),
]

# Xoay ảnh lật lại (hướng phải)
flipped_image = flip_image(image)
angle_name_pairs_right = [
    (0, "image_right.jpg"),
    (45, "image_top_right.jpg"),
    (315, "image_bottom_right.jpg"),
    (90, "image_down.jpg"),
]

# Xử lý và lưu ảnh xoay từ ảnh gốc (hướng trái)
for angle, filename in angle_name_pairs_left:
    rotated = rotate_image(image, angle)
    cv2.imwrite(filename, rotated)
    print(f"Đã lưu ảnh xoay {angle} độ vào tệp: {filename}")

# Xử lý và lưu ảnh xoay từ ảnh lật (hướng phải)
for angle, filename in angle_name_pairs_right:
    rotated = rotate_image(flipped_image, angle)
    cv2.imwrite(filename, rotated)
    print(f"Đã lưu ảnh lật và xoay {angle} độ vào tệp: {filename}")
