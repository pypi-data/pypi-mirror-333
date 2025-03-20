import requests
import pandas as pd
from io import StringIO

class WeatherDataAI:
    BASE_URL = "https://api.weatherdata.ai/get-data"

    def __init__(self, api_key):
        """Initialize with API key."""
        self.api_key = api_key
        self.headers = {"X-API-Key": self.api_key}

    def get_data(self, data_type, variable, start_date, end_date, lat, lon, units="Metric", output="dataframe", save_path=None):
        """
        Fetch weather data (observations or forecasts).

        :param data_type: "observation" or "forecast"
        :param variable: Weather variable (e.g., '2T' for temperature)
        :param start_date: Start date (YYYY-MM-DD)
        :param end_date: End date (YYYY-MM-DD)
        :param lat: Latitude
        :param lon: Longitude
        :param units: "Metric" or "Imperial" (default is "Metric")
        :param output: "dataframe" (default) or "csv" (to return raw CSV text)
        :param save_path: If provided, saves the CSV to this file path
        :return: Pandas DataFrame or raw CSV string
        """
        if data_type not in ["observation", "forecast"]:
            raise ValueError("Invalid data_type. Choose 'observation' or 'forecast'.")

        url = f"{self.BASE_URL}/{data_type}/{variable}/{start_date}/{end_date}/{lat}/{lon}/{units}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            csv_data = response.text

            # Save CSV if save_path is provided
            if save_path:
                with open(save_path, "w", encoding="utf-8") as file:
                    file.write(csv_data)
                return f"CSV file saved to {save_path}"

            # Return as raw CSV text
            if output == "csv":
                return csv_data

            # Convert to Pandas DataFrame
            csv_buffer = StringIO(csv_data)
            df = pd.read_csv(csv_buffer)
            return df
        else:
            response.raise_for_status()

    def get_observation(self, variable, start_date, end_date, lat, lon, units="Metric", output="dataframe", save_path=None):
        """Fetch observational weather data (returns CSV or Pandas DataFrame)."""
        return self.get_data("observation", variable, start_date, end_date, lat, lon, units, output, save_path)

    def get_forecast(self, variable, start_date, end_date, lat, lon, units="Metric", output="dataframe", save_path=None):
        """Fetch forecasted weather data (returns CSV or Pandas DataFrame)."""
        return self.get_data("forecast", variable, start_date, end_date, lat, lon, units, output, save_path)
