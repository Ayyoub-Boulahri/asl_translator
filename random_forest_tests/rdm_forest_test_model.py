import os
import cv2 as cv
import mediapipe as mp
import numpy as np
import joblib


print("Loading model...")

model = joblib.load("asl_model.pkl")

mp_hands = mp.solutions.hands
mp_drawings = mp.solutions.drawing_utils

data_test_path = "../dataset/asl_alphabet_test"
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    for label in os.listdir(data_test_path):
        image_path = os.path.join(data_test_path, label)
        image = cv.imread(image_path)
        rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                pred = model.predict([landmarks])[0]
                print(label, pred)