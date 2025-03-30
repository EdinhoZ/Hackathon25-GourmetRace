from rest_framework import serializers
from .models import Task, Coin, History, Basket
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model =Task
        fields = ['id','task','status']


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model =Coin
        fields = ['name','code']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model =History
        fields = ['symbol','timestamp','close','open']

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model =Basket
        fields = ['name','coins']


