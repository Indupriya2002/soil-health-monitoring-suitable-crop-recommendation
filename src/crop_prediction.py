import joblib
import pandas as pd

# Load trained model
model = joblib.load("crop_model.pkl")

# Sample input
input_data = pd.DataFrame([{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 25.5,
    "humidity": 70,
    "ph": 6.5,
    "rainfall": 120
}])

# Predict crop
prediction = model.predict(input_data)

print("Predicted Crop:", prediction[0])
