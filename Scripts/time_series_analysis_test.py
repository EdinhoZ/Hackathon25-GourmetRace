import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import numpy as np

# Load the data
df = pd.read_csv("BTCEUR_historical_data.csv", parse_dates=["timestamp"], index_col="timestamp")

# Check for missing values
df.dropna(inplace=True)

# Show first few rows
print(df.head())

# Plot the closing price
plt.figure(figsize=(10,6))
plt.plot(df['close'], label='Closing Price')
plt.title('Bitcoin Closing Price (EUR)')
plt.xlabel('Date')
plt.ylabel('Price (EUR)')
plt.legend()
plt.show()

# Check for stationarity using Augmented Dickey-Fuller test
result = adfuller(df['close'])
print(f"ADF Statistic: {result[0]}")
print(f"p-value: {result[1]}")

# If the p-value > 0.05, apply differencing to make it stationary
if result[1] > 0.05:
    df['close_diff'] = df['close'].diff().dropna()

# Fit ARIMA model (p, d, q) - Example: ARIMA(5,1,0)
model = ARIMA(df['close'], order=(5,1,0))
model_fit = model.fit()

# Forecast the next 30 days
forecast_steps = 30
forecast = model_fit.forecast(steps=forecast_steps)

# Generate future dates
future_dates = pd.date_range(df.index[-1], periods=forecast_steps+1, freq='D')[1:]

forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Price': forecast})
forecast_df.set_index('Date', inplace=True)

# Filter historical data for the year 2025
historical_2025 = df.loc[df.index.year == 2025]

# Filter forecasted data for the year 2025
forecast_2025 = forecast_df.loc[forecast_df.index.year == 2025]

# Plot historical data and predictions for 2025
plt.figure(figsize=(12, 6))
plt.plot(historical_2025.index, historical_2025['close'], label='Historical Data')
plt.plot(forecast_2025.index, forecast_2025['Predicted Price'], label='Forecast (2025)', color='red', linestyle="dashed")
plt.title('Bitcoin Price Forecast for 2025')
plt.xlabel('Date')
plt.ylabel('Price (EUR)')
plt.legend()
plt.show()
