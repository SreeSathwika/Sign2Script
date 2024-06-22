import cv2
import pickle
import mediapipe as mp
import numpy as np
import tkinter as tk
from .labels_dict import labels_dict

class GestureClassifier:
    def __init__(self):
        self.model_dict = pickle.load(open("model.p", "rb"))
        self.model = self.model_dict["model"]
        self.root = tk.Tk()

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=True, min_detection_confidence=0.3
        )

    def predict(self, frame):
        data_aux = []
        x_ = []
        y_ = []

        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(frame_rgb)
        add = False
        predicted_character=None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                )

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction = self.model.predict(
                [np.asarray(data_aux + [0] * (84 - len(data_aux)))]
            )
            predicted_character = labels_dict.get(prediction[0], "Unknown")
           

        # Create a blackboard-like image
        blackboard = np.zeros((H, 500, 3), dtype=np.uint8)  # Adjust the width as needed
        if predicted_character is not None:
            cv2.putText(blackboard, "Predicted text: " + predicted_character, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            predicted_character = "None"
            cv2.putText(blackboard, "Predicted text: None", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Combine the frame and blackboard side by side
        combined_frame = np.hstack((frame, blackboard))

        return add, predicted_character, combined_frame

  #  def speak_character(self, predicted_text):
        #tts = gTTS(text=predicted_text, lang='en')
        #tts.save("prediction.mp3")
        #os.system("start prediction.mp3")
