from django import forms
from .models import Coin, Basket, History

class CoinForm(forms.ModelForm):
    class Meta:
        model = Coin
        fields = ['name', 'code']

class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ['name', 'coins']

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ['symbol','timestamp','close','open']
