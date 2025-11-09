import os
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import joblib

print("Loading neural network model...")

# Load the trained NN model and label encoder
model = tf.keras.models.load_model("asl_nn_model.h5")
le = joblib.load("label_encoder.pkl")

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawings = mp.solutions.drawing_utils

# Path to test dataset
data_test_path = "dataset/asl_alphabet_test"

# Helper: normalize landmarks (same normalization used during training)
def normalize_landmarks(landmarks):
    landmarks = np.array(landmarks).reshape(-1, 3)
    wrist = landmarks[0]
    landmarks -= wrist
    scale = np.max(np.linalg.norm(landmarks, axis=1))
    if scale == 0 or np.isnan(scale):
        scale = 1.0
    landmarks /= scale
    return landmarks.flatten()

# Loop through test images
with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
    for label in os.listdir(data_test_path):
        image_path = os.path.join(data_test_path, label)
        image = cv2.imread(image_path)
        if image is None:
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract and normalize landmarks
                landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                normalized = normalize_landmarks(landmarks)

                # Predict using the NN model
                pred_probs = model.predict(np.array([normalized]), verbose=0)
                pred_idx = np.argmax(pred_probs)
                pred_label = le.inverse_transform([pred_idx])[0]

                print(f"True: {label} | Predicted: {pred_label}")
