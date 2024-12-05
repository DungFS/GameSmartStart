import cv2
import mediapipe as mp

class HandGestureRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
        self.camera_open = False
        self.detected_fingers = None  # Biến để lưu số ngón tay nhận diện được

    def count_fingers(self, landmarks):
        fingers = []
        tips_ids = [4, 8, 12, 16, 20]

        # Ngón cái (kiểm tra hướng x)
        if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Các ngón còn lại (kiểm tra hướng y)
        for i in range(1, 5):
            if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)

    def start_camera(self):
        self.camera_open = True
        cap = cv2.VideoCapture(0)

        # Tọa độ và kích thước của nút "OK"
        button_x, button_y, button_w, button_h = 450, 10, 100, 50

        # Hàm xử lý sự kiện nhấp chuột
        def click_event(event, x, y, flags, params):
            if event == cv2.EVENT_LBUTTONDOWN:
                # Kiểm tra nếu nhấp chuột vào vùng nút "OK"
                if button_x <= x <= button_x + button_w and button_y <= y <= button_y + button_h:
                    self.stop_camera()

        # Gắn hàm sự kiện nhấp chuột vào cửa sổ
        cv2.namedWindow("Hand Gesture Recognition")
        cv2.setMouseCallback("Hand Gesture Recognition", click_event)

        while self.camera_open:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    self.detected_fingers = self.count_fingers(hand_landmarks.landmark)
                    cv2.putText(frame, f'{self.detected_fingers}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Vẽ nút "OK" lên khung hình
            cv2.rectangle(frame, (button_x, button_y), (button_x + button_w, button_y + button_h), (0, 255, 0), -1)
            cv2.putText(frame, "OK", (button_x + 20, button_y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow("Hand Gesture Recognition", frame)

            # Kiểm tra nhấn phím 'q' để thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_camera()

        cap.release()
        cv2.destroyAllWindows()



    def stop_camera(self):
        self.camera_open = False


