import os

import joblib
import pandas as pd


def predict_crop(input_data, model_path=None):
    """Predict a suitable crop from soil and environmental data."""

    if model_path is None:
        model_path = os.getenv("CROP_MODEL_PATH", "crop_model.pkl")

    model = joblib.load(model_path)

    required_columns = [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "ph",
        "rainfall"
    ]

    if not all(column in input_data.columns for column in required_columns):
        raise ValueError("Input data is missing required columns")

    prediction = model.predict(input_data)

    return prediction[0]


if __name__ == "__main__":
    input_data = pd.DataFrame([{
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 25.5,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 120
    }])

    crop = predict_crop(input_data)

    print("Predicted Crop:", crop)
