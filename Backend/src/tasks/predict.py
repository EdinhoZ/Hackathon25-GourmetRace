from django.http import JsonResponse
import pandas as pd
from prophet import Prophet
from datetime import datetime
from .models import History, Coin

def predict_view(request):
    print("predicted")
    # Get parameters from the request
    coin_name = request.GET.get('coin', 'Bitcoin')  # Default to 'BTC' if no coin is provided
    coin_o = Coin.objects.filter(name = coin_name)
    coin = coin_o.name + "EUR"
    end_date = request.GET.get('end_date')  # Required parameter

    start_date = "2025-03-27"  # Fixed start date

    if not end_date:
        return JsonResponse({'error': 'end_date parameter is required'}, status=400)

    try:
        # Load coin-specific CSV data
        queryset = History.objects.filter(coin=coin).order_by('timestamp')

        # Convert the queryset to a pandas DataFrame
        data = pd.DataFrame(list(queryset.values('timestamp', 'close')))
        data.sort_index(inplace=True)
        data = data.rename(columns={'close': 'y'})
        data.index.name = 'ds'

        # Predict using Prophet
        model = Prophet()
        model.fit(data.reset_index())
        
        # Calculate the number of prediction days
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end_date_obj - start_date_obj).days
        
        if num_days <= 0:
            return JsonResponse({'error': 'end_date must be after start_date'}, status=400)

        # Create a dataframe for future dates
        future = model.make_future_dataframe(periods=num_days)
        forecast = model.predict(future)

        # Filter the forecast data within the timeframe
        filtered_forecast = forecast[(forecast['ds'] >= start_date) & (forecast['ds'] <= end_date)]

        # Extract x and y values
        x_values = filtered_forecast['ds'].dt.strftime("%Y-%m-%d").tolist()
        y_values = filtered_forecast['yhat'].tolist()

        # Send data to the frontend
        return JsonResponse({'x': x_values, 'y': y_values})

    except FileNotFoundError:
        return JsonResponse({'error': f"Data file for {coin} not found"}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)