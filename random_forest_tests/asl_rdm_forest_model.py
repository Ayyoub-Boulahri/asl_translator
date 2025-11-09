import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


print("Loading data...")

data = pd.read_csv("../hand_sign_data.csv")

x = data.drop("label", axis=1)
y = data["label"]


print("Splitting data...")

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print("Training model...")
model = RandomForestClassifier(n_estimators=200, random_state=42, verbose=1)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print("Accuracy : ", accuracy_score(y_test, y_pred))

print("Saving model...")
joblib.dump(model, "asl_model.pkl")
