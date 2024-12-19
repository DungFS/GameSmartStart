import pygame
import os
import sys
import threading
from camera import hand_recognition
from level1 import level1
from level2 import level2
from level3 import level3

import ctypes


class Game:
    def __init__(self):
        # Thiết lập cơ bản
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Smart Start")

        # Đặt cửa sổ ở góc trên bên trái cho Windows
        self.set_window_position()

        # Tải hình nền
        try:
            self.background = pygame.image.load('img/backgroud/00.jpg')
        except pygame.error as e:
            print(f"Không thể tải ảnh background: {e}")
            pygame.quit()
            sys.exit()

        # Thiết lập màu sắc
        self.black = (0, 0, 0)
        self.light_blue = (173, 216, 230)
        self.light_red = (255, 99, 71)
        self.dark_red = (255, 69, 0)

        # Khởi tạo font
        font_path = 'fonts/Lato-Regular.ttf'
        self.font = pygame.font.Font(font_path, 40)
        self.instruction_font = pygame.font.Font(font_path, 25)

        # Chạy menu chính
        self.main_menu()

    def set_window_position(self):
        """Chỉnh cửa sổ về góc trên bên trái trên Windows."""
        if sys.platform == "win32":
            ctypes.windll.user32.SetWindowPos(pygame.display.get_wm_info()['window'], 0, 0, 0, 0, 0, 0)

    def create_button(self, text, x, y, width, height, color):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        label = self.font.render(text, True, self.black)
        self.screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
        return rect

    def instructions_page(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        return

            self.screen.fill(self.light_blue)

            title_text = self.font.render("Help Menu", True, self.black)
            self.screen.blit(title_text, ((self.screen_width - title_text.get_width()) // 2, 30))

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

            y_offset = 100
            for line in instructions:
                instruction_text = self.instruction_font.render(line, True, self.black)
                self.screen.blit(instruction_text, (50, y_offset))
                y_offset += 30

            back_button = self.create_button("Return", self.screen_width // 2 - 75, self.screen_height - 100, 150, 50,
                                             self.light_red)
            pygame.display.update()

    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_rects[0].collidepoint(mouse_pos):
                        threading.Thread(target=hand_recognition.start_camera, daemon=True).start()
                        level1.run()
                    elif button_rects[1].collidepoint(mouse_pos):
                        threading.Thread(target=hand_recognition.start_camera, daemon=True).start()
                        level2.run()
                    elif button_rects[2].collidepoint(mouse_pos):
                        threading.Thread(target=hand_recognition.start_camera, daemon=True).start()
                        level3.run()
                    elif help_button.collidepoint(mouse_pos):
                        self.instructions_page()
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            self.screen.blit(self.background, (0, 0))

            button_width, button_height, gap = 150, 50, 20
            total_width = 3 * button_width + 2 * gap
            start_x = (self.screen_width - total_width) // 2
            y_position = self.screen_height // 2

            button_rects = [
                self.create_button("Level 1", start_x, y_position, button_width, button_height, self.light_blue),
                self.create_button("Level 2", start_x + button_width + gap, y_position, button_width, button_height,
                                   self.light_blue),
                self.create_button("Level 3", start_x + 2 * (button_width + gap), y_position, button_width,
                                   button_height, self.light_blue)
            ]

            help_button = self.create_button("Help", self.screen_width - 160, 10, 150, 50, self.light_blue)
            exit_button = self.create_button("Exit", 10, 10, 150, 50, self.dark_red)

            pygame.display.update()


if __name__ == "__main__":
    Game()
