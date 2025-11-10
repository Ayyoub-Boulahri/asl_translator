import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import joblib
import time
import threading
from subject import Subject
import pyttsx3
import subprocess
import sys


class SignModel(Subject):
    def __init__(self, model_path, encoder_path):
        super().__init__()
        self.model = tf.keras.models.load_model(model_path)
        self.le = joblib.load(encoder_path)

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.running = False
        self.text_output = ""
        self.last_prediction = None
        self.last_change_time = time.time()
        self.stable_time_required = 0.8

        self.frame = None
        self.current_prediction = None

        
        # self.engine = pyttsx3.init()
        # self.voices = self.engine.getProperty("voices")
        # self.selected_voice_id = self.voices[0].id

    def normalize_landmarks(self, landmarks):
        landmarks = np.array(landmarks).reshape(-1, 3)
        wrist = landmarks[0]
        landmarks -= wrist
        scale = np.max(np.linalg.norm(landmarks, axis=1))
        if scale == 0 or np.isnan(scale):
            scale = 1.0
        landmarks /= scale
        return landmarks.flatten()
    
    # def set_voice(self, voice_name):
    #     """Set active TTS voice by name."""
    #     for v in self.voices:
    #         if v.name == voice_name:
    #             self.selected_voice_id = v.id
    #             break
        
    
    # def speak_text_async(self, text):
    #     """Speak text in a separate process so Windows SAPI won't freeze."""
    #     if not text.strip():
    #         return

    #     def _speak():
    #         subprocess.Popen(
    #             [sys.executable, "-c",
    #                 f"import pyttsx3; e=pyttsx3.init(); e.setProperty('rate',150); "
    #                 f"e.setProperty('voice', {self.selected_voice_id!r}); e.say({text!r}); e.runAndWait()"
    #             ],
    #             stdout=subprocess.DEVNULL,
    #             stderr=subprocess.DEVNULL
    #         )

    #     threading.Thread(target=_speak, daemon=True).start()

    def start_camera(self):
        if self.running:
            return
        self.running = True
        cap = cv2.VideoCapture(0)
        threading.Thread(target=self._update_camera, args=(cap,), daemon=True).start()

    def stop_camera(self):
        self.running = False

    def clear_text(self):
        self.text_output = ""
        self.notify()

    def _update_camera(self, cap):
        with self.mp_hands.Hands(min_detection_confidence=0.5, 
                                 min_tracking_confidence=0.5) as hands:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    continue

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb)

                current_prediction = None
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                        normalized = self.normalize_landmarks(landmarks)
                        pred_probs = self.model.predict(np.array([normalized]), verbose=0)
                        pred_idx = np.argmax(pred_probs)
                        pred_label = self.le.inverse_transform([pred_idx])[0]
                        current_prediction = pred_label

                if current_prediction == self.last_prediction:
                    if time.time() - self.last_change_time >= self.stable_time_required and current_prediction:
                        if current_prediction == "del":
                            self.text_output = self.text_output[:-1]
                        elif current_prediction == "space":
                            # last_word = self.text_output.split()[-1] if self.text_output.split() else ""
                            self.text_output += " "
                            # if last_word:
                            #     print(f"Speaking word: '{last_word}'")  
                            #     self.speak_text_async(last_word)
                        else:
                            self.text_output += current_prediction
                        self.last_change_time = time.time()
                else:
                    self.last_prediction = current_prediction
                    self.last_change_time = time.time()

                self.frame = frame
                self.current_prediction = current_prediction
                self.notify()

        cap.release()
        self.frame = None
        self.notify()
