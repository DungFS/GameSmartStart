import pygame
import sys
import random


from camera import HandGestureRecognition


hand_gesture = HandGestureRecognition()


# Khởi tạo Pygame cho Level 1
def run_level2():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Level 2")
    font = pygame.font.SysFont(None, 40)

    # Tải hình ảnh background
    background = pygame.image.load('img/backgroud/01.jpg')

    # Tải các hình ảnh (6 bức ảnh có kết quả từ 0-5)
    img0 = pygame.image.load('img/level2/0-removebg-preview.png')
    img1 = pygame.image.load('img/level2/1-removebg-preview.png')
    img2 = pygame.image.load('img/level2/2-removebg-preview.png')
    img3 = pygame.image.load('img/level2/3-removebg-preview.png')
    img4 = pygame.image.load('img/level2/4-removebg-preview.png')
    img5 = pygame.image.load('img/level2/5-removebg-preview.png')

    images = [img0, img1, img2, img3, img4, img5]
    current_image = random.choice(images)
    image_index = images.index(current_image)  # Lưu chỉ số của hình ảnh hiện tại
    image_rect = current_image.get_rect(center=(400, 300))

    result = None  # Biến lưu kết quả kiểm tra

    while True:
        screen.blit(background, (0, 0))
        screen.blit(current_image, image_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Nhấn nút chuột để bật/tắt camera
            if event.type == pygame.MOUSEBUTTONDOWN:
                if camera_button.collidepoint(event.pos):
                   hand_gesture.start_camera()


                elif check_button.collidepoint(event.pos):
                    if hand_gesture.detected_fingers == image_index:
                        result = "Correct"
                    else:
                        result = f"Wrong! Detected: {hand_gesture.detected_fingers}, Expected: {image_index}"
                elif back_button.collidepoint(event.pos):
                    return  # Thoát khỏi level, quay lại menu chính

                elif next_button.collidepoint((event.pos)):
                    current_image = random.choice(images)
                    image_index = images.index(current_image)
                    result = ""

        # Hiển thị nút "Bật/Tắt Camera" và "Kiểm tra kết quả"
        camera_button = create_button(screen, "Open Camera", 150, 500, 200, 50, (173, 216, 230), font)
        check_button = create_button(screen, "Check", 450, 500, 200, 50, (173, 216, 230), font)
        back_button = create_button(screen, "Menu", 20, 20, 200, 50, (173, 216, 230), font)
        next_button = create_button(screen, "Next", 580, 20, 200, 50, (173, 216, 230), font)
        # Hiển thị kết quả nếu có
        if result:
            result_label = font.render(f"{result}", True, (0, 0, 0))
            screen.blit(result_label, (400 - result_label.get_width() // 2, 100))

        pygame.display.update()


def create_button(screen, text, x, y, width, height, color, font):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=15)
    label = font.render(text, True, (0, 0, 0))
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
    return rect
