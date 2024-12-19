import cv2
import mediapipe as mp
import queue

class HandGestureRecognition:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
        self.result_queue = queue.Queue()
        self.cap = cv2.VideoCapture(0)
        self.run = True

    def detect_fingers(self, landmarks):
        """Detect the number of fingers raised."""
        fingers = []
        tips_ids = [4, 8, 12, 16, 20]

        # Thumb (check x direction)
        if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers (check y direction)
        for i in range(1, 5):
            if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)

    def stop_camera(self):
        """Stop the camera and release resources."""
        self.cap.release()
        cv2.destroyAllWindows()

    def start_camera(self):
        camera_open = True
        self.cap = cv2.VideoCapture(0)
        while camera_open:
            ret, frame = self.cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    detected_fingers = self.detect_fingers(hand_landmarks.landmark)
                    cv2.putText(frame, f'{detected_fingers}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Store the result in the queue
                    self.result_queue.put(detected_fingers)

            cv2.imshow("Hand Gesture Recognition", frame)

            # Check for key press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                camera_open = False
        self.stop_camera()
hand_recognition = HandGestureRecognition()


