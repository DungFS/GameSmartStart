import pygame
import sys
import random

from camera import hand_recognition


class Level3:
    def __init__(self):
        # Khởi tạo Pygame cho Level 3
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Level 3")
        self.font = pygame.font.SysFont(None, 60)

        # Tải hình ảnh background
        self.background = pygame.image.load('img/backgroud/01.jpg')

        # Khởi tạo câu hỏi và kết quả
        self.question, self.correct_answer = self.generate_question()
        self.correct_answer_time = None  # Thời gian trả lời đúng
        self.result_message = ""  # Thông báo đúng/sai
        self.waiting_for_new_image = False  # Trạng thái chờ đổi hình ảnh

    def generate_question(self):
        while True:
            num1 = random.randint(0, 5)
            num2 = random.randint(0, 5)
            operation = random.choice(['+', '-'])
            result = num1 + num2 if operation == '+' else num1 - num2
            if 0 <= result <= 5:
                return f"{num1} {operation} {num2}", result

    def create_button(self, text, x, y, width, height, color):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        label = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
        return rect

    def check_camera_input(self):
        """Kiểm tra đầu vào từ camera."""
        if not hand_recognition.result_queue.empty() and not self.waiting_for_new_image:
            detected_result = hand_recognition.result_queue.get()
            if detected_result == self.correct_answer:  # Nếu trả lời đúng
                self.correct_answer_time = pygame.time.get_ticks()
                self.result_message = "\u0110\u00fang!"
                self.waiting_for_new_image = True
            else:
                self.result_message = "Sai!"

    def update_image(self):
        """Cập nhật hình ảnh sau khi trả lời đúng."""
        if self.waiting_for_new_image and self.correct_answer_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.correct_answer_time >= 2500:  # 2500 ms = 2.5 giây
                self.question, self.correct_answer = self.generate_question()
                self.correct_answer_time = None
                self.result_message = ""
                self.waiting_for_new_image = False

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            # Hiển thị câu hỏi phép toán
            question_label = self.font.render(self.question + " = ?", True, (0, 0, 0))
            self.screen.blit(question_label, (400 - question_label.get_width() // 2, 250))

            self.check_camera_input()
            self.update_image()

            # Hiển thị nút quay lại
            back_button = self.create_button("Menu", 20, 20, 200, 50, (173, 216, 230))
            # Hiển thị thông báo đúng/sai
            result_label = self.font.render(
                self.result_message, True, (0, 255, 0) if self.result_message == "\u0110\u00fang!" else (255, 0, 0)
            )
            self.screen.blit(result_label, (400 - result_label.get_width() // 2, 500))
            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        hand_recognition.stop_camera()
                        return  # Thoát khỏi level, quay lại menu chính

            pygame.display.update()

# Hàm khởi chạy level 3
level3 = Level3()

