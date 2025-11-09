import pandas as pd
import numpy as np

df = pd.read_csv("hand_sign_data.csv")

def normalize_row(row):
    # drop label if it exists in row
    features = row[:-1] if not isinstance(row.iloc[-1], (int, float)) else row
    try:
        coords = np.array(features, dtype=float).reshape(-1, 3)
    except Exception:
        return [np.nan] * (len(features)) + [row.iloc[-1]]  # skip bad rows

    wrist = coords[0]
    coords -= wrist
    scale = np.max(np.linalg.norm(coords, axis=1))
    if scale == 0 or np.isnan(scale):
        scale = 1.0
    coords /= scale
    return coords.flatten().tolist() + [row.iloc[-1]]

normalized = df.apply(normalize_row, axis=1, result_type='expand')

# remove any bad rows
normalized = normalized.dropna()

normalized.to_csv("train_landmarks_normalized.csv", index=False)
print("Saved normalized CSV with shape:", normalized.shape)
