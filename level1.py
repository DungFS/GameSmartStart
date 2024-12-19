import pygame
import sys
import random
from camera import hand_recognition

class Level1:
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Level 1")
        self.font = pygame.font.SysFont(None, 40)

        # Tải hình ảnh background
        self.background = pygame.image.load('img/backgroud/01.jpg')

        # Tải các hình ảnh (6 bức ảnh có kết quả từ 0-5)
        self.images = [
            pygame.image.load(f'img/level1/{i}-removebg-preview.png') for i in range(6)
        ]
        self.current_image = random.choice(self.images)
        self.image_index = self.images.index(self.current_image)
        self.image_rect = self.current_image.get_rect(center=(400, 300))

        # Biến trạng thái
        self.correct_answer_time = None  # Thời gian trả lời đúng
        self.result_message = ""  # Thông báo đúng/sai
        self.waiting_for_new_image = False  # Trạng thái chờ đổi hình ảnh

    def create_button(self, text, x, y, width, height, color):
        """Tạo nút bấm trên màn hình."""
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        label = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(
            label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2)
        )
        return rect

    def check_camera_input(self):
        """Kiểm tra đầu vào từ camera."""
        if not hand_recognition.result_queue.empty() and not self.waiting_for_new_image:
            detected_result = hand_recognition.result_queue.get()
            if detected_result == self.image_index:  # Nếu trả lời đúng
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
                self.current_image = random.choice(self.images)
                self.image_index = self.images.index(self.current_image)
                self.correct_answer_time = None
                self.result_message = ""
                self.waiting_for_new_image = False

    def run(self):
        """Chạy Level 1."""
        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.current_image, self.image_rect)

            self.check_camera_input()
            self.update_image()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        hand_recognition.stop_camera()
                        return  # Quay lại menu chính

            # Hiển thị nút "Menu"
            self.back_button = self.create_button("Menu", 20, 20, 200, 50, (173, 216, 230))

            # Hiển thị thông báo đúng/sai
            result_label = self.font.render(
                self.result_message, True, (0, 255, 0) if self.result_message == "\u0110\u00fang!" else (255, 0, 0)
            )
            self.screen.blit(result_label, (400 - result_label.get_width() // 2, 500))

            pygame.display.update()

level1 = Level1()

