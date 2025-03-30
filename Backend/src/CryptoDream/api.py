from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Task, Coin, History, Basket
from .serializer import TaskSerializer, CoinSerializer, HistorySerializer, BasketSerializer

class TaskListApi(ListAPIView):
    queryset = Task.objects.all()
    serializer_class =  TaskSerializer
    
class CreateTaskApi(CreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

class RetrieveUpdateDestroyTaskApi(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class =  TaskSerializer
    

class BasketListApi(ListAPIView):
    queryset = Basket.objects.all()
    serializer_class =  BasketSerializer

class CreateBasketApi(CreateAPIView):
    queryset = Basket.objects.all()
    serializer_class =  BasketSerializer


class RetrieveUpdateDestroyBasketApi(RetrieveUpdateDestroyAPIView):
    queryset = Basket.objects.all()
    serializer_class =  BasketSerializer


'''
class TaskListApi(ListAPIView):
    queryset = Coin.objects.all()
    serializer_class =  CoinSerializer

class CoinListApi(CreateAPIView):
    queryset = Coin.objects.all()
    serializer_class =  CoinSerializer


class RetrieveUpdateDestroyTaskApi(RetrieveUpdateDestroyAPIView):
    queryset = Coin.objects.all()
    serializer_class =  CoinSerializer
    


class TaskListApi(ListAPIView):
    queryset = History.objects.all()
    serializer_class =  HistorySerializer

class HistoryListApi(CreateAPIView):
    queryset = History.objects.all()
    serializer_class =  HistorySerializer
    

class RetrieveUpdateDestroyTaskApi(RetrieveUpdateDestroyAPIView):
    queryset = History.objects.all()
    serializer_class =  HistorySerializer
'''