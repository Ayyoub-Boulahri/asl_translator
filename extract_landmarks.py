import os
import csv
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

def extract_landmarks(data_path, output_csv="output.csv"):
    with open(output_csv, mode="w", newline='') as f:
        writer = csv.writer(f)
        header = []
        for i in range(21):
            header += [f'x{i}', f'y{i}', f'z{i}']
        header.append('label')
        writer.writerow(header)

        with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
            for label in sorted(os.listdir(data_path)):
                folder = os.path.join(data_path, label)
                if not os.path.isdir(folder):
                    continue
                
                for file_name in os.listdir(folder):
                    file_path = os.path.join(folder, file_name)
                    image = cv2.imread(file_path)
                    if image is None:
                        continue

                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image_rgb)
                    if not results.multi_hand_landmarks:
                        continue

                    landmarks = results.multi_hand_landmarks[0].landmark
                    row = []

                    for lm in landmarks:
                        row.extend([lm.x, lm.y, lm.z])
                    row.append(label)
                    writer.writerow(row)


extract_landmarks("dataset/asl_alphabet_train", "hand_sign_data.csv")