import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import joblib
import time

# --- Load NN model and label encoder ---
model = tf.keras.models.load_model("asl_nn_model.h5")
le = joblib.load("label_encoder.pkl")

# --- Mediapipe setup ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# --- Helper: normalize landmarks ---
def normalize_landmarks(landmarks):
    landmarks = np.array(landmarks).reshape(-1, 3)
    wrist = landmarks[0]
    landmarks -= wrist  # position normalization
    scale = np.max(np.linalg.norm(landmarks, axis=1))
    if scale == 0 or np.isnan(scale):
        scale = 1.0
    landmarks /= scale
    return landmarks.flatten()

# --- Webcam setup ---
cap = cv2.VideoCapture(0)

text_output = ""           # collected text
last_prediction = None
last_change_time = time.time()
stable_time_required = 2.0  # seconds of stability before accepting a letter

with mp_hands.Hands(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        current_prediction = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract and normalize landmarks
                landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                normalized = normalize_landmarks(landmarks)

                # Predict using the NN model
                pred_probs = model.predict(np.array([normalized]), verbose=0)
                pred_idx = np.argmax(pred_probs)
                pred_label = le.inverse_transform([pred_idx])[0]
                current_prediction = pred_label

        # --- Stability check ---
        if current_prediction == last_prediction:
            if time.time() - last_change_time >= stable_time_required and current_prediction is not None:
                if current_prediction == "del":
                    text_output = text_output[:-1]
                elif current_prediction == "space":
                    text_output += " "
                else:
                    text_output += current_prediction
                print("Word so far:", text_output)
                last_change_time = time.time()
        else:
            last_prediction = current_prediction
            last_change_time = time.time()

        # --- Display on frame ---
        cv2.putText(frame, f"Sign: {current_prediction}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        cv2.putText(frame, f"Text: {text_output}", (50, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

        cv2.imshow("ASL Writer (NN Model)", frame)

        # Exit on ESC
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
