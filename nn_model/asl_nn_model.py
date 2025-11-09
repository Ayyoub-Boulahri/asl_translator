import tensorflow as tf
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

data = pd.read_csv("train_landmarks_normalized.csv")
data.rename(columns={data.columns[-1]: 'label'}, inplace=True)

x = data.drop("label", axis=1)
y = data["label"]


le = LabelEncoder()
y_enc = le.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y_enc, test_size=0.2, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu', input_shape=(x_train.shape[1],)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(len(le.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, validation_split=0.2, epochs=30, batch_size=64)

model.save("asl_nn_model.h5")

joblib.dump(le, "label_encoder.pkl")

print("Model and label encoder saved.")