import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from prophet import Prophet
from datetime import datetime, timedelta

def calculate_end_date(start_date, num_days):
    """
    Calculates the end date given a start date and a number of days.

    Parameters:
    - start_date (str): The starting date in "YYYY-MM-DD" format.
    - num_days (int): The number of days to add to the start date.

    Returns:
    - str: The calculated end date in "YYYY-MM-DD" format.
    """
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = start_date_obj + timedelta(days=float(num_days))
    return end_date_obj.strftime("%Y-%m-%d")


def plot_forecast_within_timeframe(forecast, start_date, end_date):
    """
    Plots the future predictions within a given timeframe.

    Parameters:
    - forecast: DataFrame containing the forecasted values (must include 'ds' and 'yhat').
    - start_date: Start date (string or datetime) of the timeframe.
    - end_date: End date (string or datetime) of the timeframe.
    """
    # Filter the forecast dataframe within the specified timeframe
    filtered_forecast = forecast[(forecast['ds'] >= start_date) & (forecast['ds'] <= end_date)]
    
    # Plot the filtered data
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_forecast['ds'], filtered_forecast['yhat'], label='Filtered Predictions', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Predicted Prices')
    plt.title(f'Predictions Between {start_date} and {end_date}')
    plt.legend()
    plt.grid()
    plt.show()
from datetime import datetime, timedelta
import plotly.graph_objects as go

def get_forecast_data(forecast, start_date, num_days):
    """
    Filters forecast data within a given timeframe calculated using start date and number of days.

    Parameters:
    - forecast: DataFrame containing the forecasted values (must include 'ds' and 'yhat').
    - start_date: Start date (string or datetime) in "YYYY-MM-DD" format.
    - num_days: Number of days to include in the forecast.

    Returns:
    - DataFrame: Filtered forecast data within the calculated timeframe.
    """
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = start_date_obj + timedelta(days=num_days)
    end_date = end_date_obj.strftime("%Y-%m-%d")
    
    # Filter forecast data between start_date and end_date
    filtered_forecast = forecast[(forecast['ds'] >= start_date) & (forecast['ds'] <= end_date)]
    return filtered_forecast

def plot_forecast_with_plotly(filtered_forecast):
    """
    Plots the filtered forecast data using Plotly.

    Parameters:
    - filtered_forecast: DataFrame containing filtered forecast data (must include 'ds' and 'yhat').
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_forecast['ds'],
        y=filtered_forecast['yhat'],
        mode='lines',
        name='Predicted Prices'
    ))
    fig.update_layout(
        title="Future Stock Price Predictions",
        xaxis_title="Date",
        yaxis_title="Predicted Prices",
        template="plotly"
    )
    fig.show()

# Example Usage
start_date = "2025-03-30"
num_days = 30


# Load your stock data (ensure it has a 'timestamp' and 'close' column)


def predict_future_values(coin, days):
    csv_path = "XRPEUR_historical_data.csv"
    # Read the CSV, parse 'timestamp' column as datetime, and set it as the index
    data = pd.read_csv(
        csv_path,
        parse_dates=["timestamp"],
        dayfirst=True,  # Adjust as per the date format in your dataset
        index_col="timestamp"
    )

    # Sort the data by date (optional, but good practice)
    data.sort_index(inplace=True)

    # Rename columns for Prophet compatibility
    data = data.rename(columns={'close': 'y'})  # Prophet requires 'y' for values
    data.index.name = 'ds'  # Prophet requires 'ds' for date

    # Initialize the Prophet model
    model = Prophet()
    model.fit(data.reset_index())  # Reset index since Prophet doesn't use a datetime index directly

    # Create a dataframe for future dates
    future_horizon = 30  # Number of days to predict into the future
    future = model.make_future_dataframe(periods=future_horizon)

    # Forecast the future values
    forecast = model.predict(future)

    # Plot the results
    model.plot(forecast)
    start_date = '2025-03-30'
    end_date = calculate_end_date(start_date, days)
    plot_forecast_within_timeframe(forecast, start_date, end_date)

    # Display the forecast for future dates
    future_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(future_horizon)
    print(future_forecast)

    filtered_forecast = get_forecast_data(forecast, start_date, num_days)
    print(plot_forecast_with_plotly(filtered_forecast))

predict_future_values("XRPEUR", 30)