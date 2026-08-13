import requests


def test_sensor_api_returns_response():
    url = "http://127.0.0.1:8000/sensor"

    response = requests.get(url)

    assert response.status_code == 200
