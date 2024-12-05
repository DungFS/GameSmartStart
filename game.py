import pygame
import sys
from scipy.constants import light_year
import level1
import level2
import level3

# Khởi tạo Pygame
pygame.init()

# Tạo kích thước màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Đặt tiêu đề cho cửa sổ
pygame.display.set_caption("Smart Start ")

# Tải hình ảnh background từ thư viện có sẵn
try:
    background = pygame.image.load('img/backgroud/00.jpg')
except pygame.error as e:
    print(f"Không thể tải ảnh background: {e}")
    pygame.quit()
    sys.exit()

# Thiết lập màu sắc
black = (0, 0, 0)
light_blue = (173, 216, 230)  # Xanh dương nhạt
light_red = (255, 99, 71)  # Màu đỏ tươi cho nút
dark_red = (255, 69, 0)  # Màu đỏ đậm cho nút Thoát

# Khởi tạo font chữ
font_path = 'fonts/Lato-Regular.ttf'
font = pygame.font.SysFont(None, 40)

# Hàm để tạo nút
def create_button(text, x, y, width, height, color):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=15)  # Tạo hình chữ nhật góc cong
    label = font.render(text, True, black)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
    return rect

# Hàm để xử lý sự kiện khi nhấp chuột
def button_click_check(button_rects, pos):
    for idx, rect in enumerate(button_rects):
        if rect.collidepoint(pos):  # Kiểm tra nếu vị trí nhấp chuột nằm trong nút
            return idx + 1  # Trả về số level (1, 2, hoặc 3)
    return None

# Trang Hướng dẫn
def instructions_page():
    while True:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):  # Quay lại menu chính
                    return

        # Vẽ nền trang Hướng dẫn
        screen.fill(light_blue)

        # Hiển thị tiêu đề
        title_text = font.render("Help Menu", True, black)
        screen.blit(title_text, ((screen_width - title_text.get_width()) // 2, 30))

        # Hiển thị nội dung từng mức độ
        instructions = [
            "Level 1: Recognize numbers from images",
            "  - Observe the image and identify the number of fingers shown.",
            "  - Raise your hand to the camera for detection.",
            "",
            "Level 2: Complete the missing sequence",
            "  - Find the missing number in the sequence.",
            "  - Choose the correct number to complete it.",
            "",
            "Level 3: Solve basic math problems",
            "  - Solve addition, subtraction, multiplication, or division (0-5).",
            "  - Enter the result or use hand gestures (if supported).",
        ]

        # Khởi tạo font với kích thước nhỏ hơn cho phần hướng dẫn
        instruction_font = pygame.font.Font(font_path, 25)  # Giảm kích thước font xuống 25
        y_offset = 100
        for line in instructions:
            instruction_text = instruction_font.render(line, True, black)
            screen.blit(instruction_text, (50, y_offset))
            y_offset += 30  # Khoảng cách giữa các dòng (giảm xuống)

        # Tạo nút "Quay lại" với màu nền mới
        back_button = create_button("Return", screen_width // 2 - 75, screen_height - 100, 150, 50, light_red)  # Màu đỏ tươi

        # Cập nhật màn hình
        pygame.display.update()

# Vòng lặp menu chính
def main_menu():
    while True:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                clicked_button = button_click_check(button_rects, mouse_pos)
                if clicked_button == 1:
                    level1.run_level1()  # Chạy level 1
                elif clicked_button == 2:
                    level2.run_level2()  # Chạy level 2
                elif clicked_button == 3:
                    level3.run_level3()  # Chạy level 3
                elif event.pos[0] >= screen_width - 160 and event.pos[1] <= 60:  # Kiểm tra nút Hướng dẫn
                    instructions_page()  # Chuyển sang trang Hướng dẫn
                elif event.pos[0] <= 160 and event.pos[1] <= 60:  # Kiểm tra nút Thoát
                    pygame.quit()
                    sys.exit()

        # Vẽ background lên màn hình
        screen.blit(background, (0, 0))

        # Tạo các nút Level ở giữa
        button_width = 150
        button_height = 50
        gap = 20  # Khoảng cách giữa các nút
        total_width = 3 * button_width + 2 * gap  # Tổng chiều rộng của 3 nút và khoảng cách
        start_x = (screen_width - total_width) // 2
        y_position = screen_height // 2

        button_rects = []  # Lưu vị trí các nút
        button_rects.append(create_button("Level 1", start_x, y_position, button_width, button_height, light_blue))
        button_rects.append(create_button("Level 2", start_x + button_width + gap, y_position, button_width, button_height, light_blue))
        button_rects.append(create_button("Level 3", start_x + 2 * (button_width + gap), y_position, button_width, button_height, light_blue))

        # Tạo nút Hướng dẫn ở góc phải màn hình
        create_button("Help", screen_width - 160, 10, 150, 50, light_blue)

        # Tạo nút Thoát ở góc trái màn hình
        create_button("Exit", 10, 10, 150, 50, dark_red)

        # Cập nhật màn hình
        pygame.display.update()

# Chạy menu chính
main_menu()
