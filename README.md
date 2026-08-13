# Soil Health Monitoring and Crop Recommendation System

An IoT and machine learning based system for monitoring soil conditions and recommending suitable crops based on soil nutrient and environmental parameters.

## Project Overview

The system combines soil sensing, weather data, machine learning, and a Streamlit-based user interface to provide crop recommendations.

The project collects NPK values from a soil sensor connected to an Arduino through RS485 communication. Environmental information such as temperature, humidity, and rainfall is also used. The collected information is processed and used for crop recommendation.

## System Workflow

Soil NPK Sensor
        ↓
Arduino + RS485
        ↓
Python Backend
        ↓
Weather Data
        ↓
Machine Learning Model
        ↓
Crop Recommendation
        ↓
Streamlit User Interface

## Features

- Real-time NPK soil data collection
- RS485 and Modbus communication
- Weather API integration
- Machine learning based crop recommendation
- Soil nutrient status display
- Chemical and organic fertilizer recommendations
- Alternative crop recommendations
- Crop nutrient requirement lookup
- Multilingual user interface
- Text-to-speech output

## Technologies Used

- Python
- Pandas
- Scikit-learn
- Joblib
- Streamlit
- REST API
- Requests
- Arduino
- RS485
- Modbus
- NPK Sensor
- I2C LCD
- PySerial
- Google Translator
- gTTS
- Pytest

## Repository Structure

```text
├── app/
│   └── streamlit_app.py
│
├── arduino/
│   └── npk_sensor.ino
│
├── src/
│   ├── crop_prediction.py
│   ├── sensor_reader.py
│   └── weather_api.py
│
├── tests/
│   ├── test_prediction.py
│   └── test_api.py
│
├── crop_dataset.csv
├── requirements.txt
└── README.md
