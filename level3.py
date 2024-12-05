import pygame
import sys
import random
from camera import HandGestureRecognition

# Khởi tạo đối tượng nhận diện cử chỉ tay
hand_gesture = HandGestureRecognition()


# Khởi tạo Pygame cho Level 3
def run_level3():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Level 3")
    font = pygame.font.SysFont(None, 60)

    # Tải hình ảnh background
    background = pygame.image.load('img/backgroud/01.jpg')

    # Tạo phép toán ngẫu nhiên với kết quả trong khoảng 0-5
    def generate_question():
        while True:
            num1 = random.randint(0, 5)
            num2 = random.randint(0, 5)
            operation = random.choice(['+', '-'])
            result = num1 + num2 if operation == '+' else num1 - num2
            if 0 <= result <= 5:
                return f"{num1} {operation} {num2}", result

    question, correct_answer = generate_question()
    result_text = None  # Biến lưu kết quả kiểm tra

    while True:
        screen.blit(background, (0, 0))

        # Hiển thị câu hỏi phép toán
        question_label = font.render(question + " = ?", True, (0, 0, 0))
        screen.blit(question_label, (400 - question_label.get_width() // 2, 250))

        # Hiển thị kết quả nếu có
        if result_text:
            result_label = font.render(result_text, True, (0, 0, 0))
            screen.blit(result_label, (400 - result_label.get_width() // 2, 100))

        # Hiển thị các nút
        camera_button = create_button(screen, "Open Camera", 150, 500, 200, 50, (173, 216, 230), font)
        check_button = create_button(screen, "Check", 450, 500, 200, 50, (173, 216, 230), font)
        back_button = create_button(screen, "Menu", 20, 20, 200, 50, (173, 216, 230), font)
        next_button = create_button(screen, "Next", 580, 20, 200, 50, (173, 216, 230), font)

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if camera_button.collidepoint(event.pos):
                    hand_gesture.start_camera()
                elif check_button.collidepoint(event.pos):
                    detected_value = hand_gesture.detected_fingers
                    if detected_value == correct_answer:
                        result_text = "Correct"
                    else:
                        result_text = f"Wrong! Detected: {detected_value}, Expected: {correct_answer}"
                elif back_button.collidepoint(event.pos):
                    return  # Thoát khỏi level, quay lại menu chính
                elif next_button.collidepoint(event.pos):
                    question, correct_answer = generate_question()
                    result_text = ""

        pygame.display.update()


def create_button(screen, text, x, y, width, height, color, font):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=15)
    label = font.render(text, True, (0, 0, 0))
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
    return rect
