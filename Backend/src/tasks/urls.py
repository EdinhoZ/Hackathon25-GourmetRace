from django.contrib import admin
from django.urls import path,include
from .api import TaskListApi,RetrieveUpdateDestroyTaskApi,CreateTaskApi
from .views import predict_future_values
from .predict import predict_view
urlpatterns = [
    path('',TaskListApi.as_view()),
    path('editTask/<int:pk>',RetrieveUpdateDestroyTaskApi.as_view()),
    path('create/',CreateTaskApi.as_view()),
    path('predict/', predict_view, name='predict_view'),
    path('forecast/', predict_future_values, name='forecast')
]