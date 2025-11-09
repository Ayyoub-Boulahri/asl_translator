import cv2
import mediapipe as mp
import numpy as np
import joblib
import time

model = joblib.load("asl_model.pkl")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


text_output = ""           # what the model "writes"
last_prediction = None     # last detected letter
last_change_time = time.time()
stable_time_required = 2.0  # seconds to wait before confirming letter

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
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

                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
                pred = model.predict([landmarks])[0]
                current_prediction = pred

        # Check stability
        if current_prediction == last_prediction:
            if time.time() - last_change_time >= stable_time_required and current_prediction is not None:
                if current_prediction == "del":
                    text_output = text_output[:-1]
                elif current_prediction == "space":
                    text_output += " "
                else :
                    text_output += current_prediction
                print("Word so far:", text_output)
                last_change_time = time.time()  # reset timer to avoid duplicate writing
        else:
            last_prediction = current_prediction
            last_change_time = time.time()

        # Display
        cv2.putText(frame, f"Sign: {current_prediction}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        cv2.putText(frame, f"Text: {text_output}", (50, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

        cv2.imshow("ASL Writer", frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
