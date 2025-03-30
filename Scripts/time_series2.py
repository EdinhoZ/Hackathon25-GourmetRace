import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
import numpy as np

# Define the path to your CSV file
# You may have to make this path more specific to the location of your file.
csv_path = "BTCEUR_historical_data.csv"

# Read the CSV, parse 'Date' column as datetime, and set it as the index
data = pd.read_csv(
    csv_path,
    parse_dates=["timestamp"],
    dayfirst=False,
    index_col="timestamp"
)

# Sort the DataFrame by the Date index in ascending order
data.sort_index(inplace=True)

# Perform the Augmented Dickey-Fuller test on the original series
result_original = adfuller(data["close"])

print(f"ADF Statistic (Original): {result_original[0]:.4f}")
print(f"p-value (Original): {result_original[1]:.4f}")

if result_original[1] < 0.05:
    print("Interpretation: The original series is Stationary.\n")
else:
    print("Interpretation: The original series is Non-Stationary.\n")

# Apply first-order differencing
data['close_Diff'] = data['close'].diff()

# Perform the Augmented Dickey-Fuller test on the differenced series
result_diff = adfuller(data["close_Diff"].dropna())
print(f"ADF Statistic (Differenced): {result_diff[0]:.4f}")
print(f"p-value (Differenced): {result_diff[1]:.4f}")
if result_diff[1] < 0.05:
    print("Interpretation: The differenced series is Stationary.")
else:
    print("Interpretation: The differenced series is Non-Stationary.")

plt.figure(figsize=(14, 7))
plt.plot(data.index, data['close_Diff'], label='Differenced close Price', color='orange')
plt.title('Differenced close Price Over Time')
plt.xlabel('Date')
plt.ylabel('Differenced close Price')
plt.legend()
plt.show()

# Plot ACF and PACF for the differenced series
fig, axes = plt.subplots(1, 2, figsize=(16, 4))

# ACF plot
plot_acf(data['close_Diff'].dropna(), lags=40, ax=axes[0])
axes[0].set_title('Autocorrelation Function (ACF)')

# PACF plot
plot_pacf(data['close_Diff'].dropna(), lags=40, ax=axes[1])
axes[1].set_title('Partial Autocorrelation Function (PACF)')

plt.tight_layout()
plt.show()

# Split data into train and test
#train_size = int(len(data) * 0.8)
train = data.iloc[:-1]

# Create the date range for the forecast (next 31 days starting from a specific date)
start_date = "2025-04-01"
date_range = pd.date_range(start=start_date, periods=400, freq='D')

# Create DataFrame for future dates
df2 = pd.DataFrame({'timestamp': date_range})

# Fit ARIMA model
model = ARIMA(train["close"], order=(5,1,0))
model_fit = model.fit()

# Forecast the next 31 days (as specified by the length of `df2`)
forecast = model_fit.forecast(steps=len(df2))

# Create a DataFrame for the forecasted values with corresponding dates
forecast_df = pd.DataFrame({'timestamp': date_range, 'forecast': forecast})

display_df = train.iloc[int(len(train)*0.9):]  # Fixing the float index to integer
# Plot the results
plt.figure(figsize=(14,7))
plt.plot(display_df.index, display_df["close"], label='Train', color='#203147')
plt.plot(forecast_df["timestamp"], forecast_df["forecast"], label='Forecast', color='#01ef63')
plt.title('Bitcoin Price Forecast')
plt.xlabel('Date')
plt.ylabel('Price (EUR)')
plt.legend()
plt.show()

print(f"AIC: {model_fit.aic}")
print(f"BIC: {model_fit.bic}")

#forecast = forecast[:len(test)]
#test_close = test["close"][:len(forecast)]

#rmse = np.sqrt(mean_squared_error(test_close, forecast))
#print(f"RMSE: {rmse:.4f}")