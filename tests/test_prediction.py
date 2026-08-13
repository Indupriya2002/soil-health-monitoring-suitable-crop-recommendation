import pandas as pd


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
