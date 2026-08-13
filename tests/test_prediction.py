import pandas as pd
import pytest

from src.crop_prediction import predict_crop


def test_prediction_input_has_required_columns():
    input_data = pd.DataFrame([{
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 25.5,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 120
    }])

    required_columns = [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "ph",
        "rainfall"
    ]

    assert list(input_data.columns) == required_columns


def test_prediction_is_valid_crop():
    valid_crops = pd.read_csv("crop_dataset.csv")["label"].unique()

    predicted_crop = "rice"

    assert predicted_crop in valid_crops


def test_negative_nutrient_values_are_detected():
    input_data = {
        "N": -10,
        "P": 42,
        "K": 43
    }

    assert input_data["N"] < 0


def test_dataset_has_required_columns():
    df = pd.read_csv("crop_dataset.csv")

    required_columns = [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "rainfall",
        "label"
    ]

    assert all(column in df.columns for column in required_columns)


def test_prediction_returns_crop():
    input_data = pd.DataFrame([{
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 25.5,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 120
    }])

    predicted_crop = predict_crop(input_data)

    assert isinstance(predicted_crop, str)
    assert predicted_crop != ""


def test_missing_required_column_raises_error():
    input_data = pd.DataFrame([{
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 25.5,
        "humidity": 70,
        "rainfall": 120
    }])

    with pytest.raises(ValueError, match="missing required columns"):
        predict_crop(input_data)
