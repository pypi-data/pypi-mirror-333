# py_weatherdataai - WeatherDataAI API Client

A simple Python client for accessing WeatherDataAI's API.

## Installation

pip install py_weatherdataai

## Usage
from py_weatherdataai.client import WeatherDataAI

api_key = "your_api_key_here"
client = WeatherDataAI(api_key)

# Get observational data as a Pandas DataFrame
df = client.get_observation("2T", "2024-02-15", "2024-02-20", -0.125, -49.625, units="Metric")
print(df)

# Get forecast data and save it as a CSV file
client.get_forecast("2T", "2024-03-15", "2024-03-20", -0.125, -49.625, units="Metric", save_path="forecast.csv")

# Get raw CSV text instead of a DataFrame
csv_text = client.get_forecast("2T", "2024-03-15", "2024-03-20", -0.125, -49.625, units="Metric", output="csv")
print(csv_text)


