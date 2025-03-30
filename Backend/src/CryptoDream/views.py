from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta
import os
from .models import Coin, History
from .forms import CoinForm  

def coin_list(request):
    coins = Coin.objects.all()
    return render(request, 'coins/coin_list.html', {'coins': coins})

def coin_create(request):
    if request.method == 'POST':
        form = CoinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coin_list')
    else:
        form = CoinForm()
    return render(request, 'coins/coin_form.html', {'form': form})

def coin_update(request, pk):
    coin = get_object_or_404(Coin, pk=pk)
    if request.method == 'POST':
        form = CoinForm(request.POST, instance=coin)
        if form.is_valid():
            form.save()
            return redirect('coin_list')
    else:
        form = CoinForm(instance=coin)
    return render(request, 'coins/coin_form.html', {'form': form})

def coin_delete(request, pk):
    coin = get_object_or_404(Coin, pk=pk)
    if request.method == 'POST':
        coin.delete()
        return redirect('coin_list')
    return render(request, 'coins/coin_confirm_delete.html', {'coin': coin})

def predict_future_values(request, coin_name):
    print(request)
    print(coin_name)
    #coin_name = request.GET.get('coin_name')
    dict = {
    "Bitcoin": "BTCEUR",
    "Ethereum": "ETHEUR",
    "BNB": "BNBEUR",
    "XPR": "XPREUR",
    "Cardano": "ADAEUR",
    "Tether": "ADAEUR",
    "Solana": "SOLEUR",
    "USD Coin": "TRXEUR",
    "Dogecoin": "DOGEEUR",
    "Tron": "TRXEUR"
}
    if coin_name not in dict:
        coin_name = "Bitcoin"
    csv_path = os.path.join(os.path.dirname(__file__), f"{dict[coin_name]}_historical_data.csv")
    data = pd.read_csv(
        csv_path,
        parse_dates=["timestamp"],
        dayfirst=True,
        index_col="timestamp"
    )

    # Drop the 'coin' column if it exists
    if 'symbol' in data.columns:
        data.drop(columns=['symbol'], inplace=True)
    
    data = data.rename(columns={'close': 'y'})
    data.index.name = 'ds'

    model = Prophet()
    model.fit(data.reset_index())

    future_horizon = 30
    future = model.make_future_dataframe(periods=future_horizon)

    forecast = model.predict(future)

    forecast_future = forecast[forecast['ds'] > data.index[-1]]

    forecast_json = forecast_future[['ds', 'yhat']].to_dict(orient='records')

    return JsonResponse(forecast_json, safe=False)