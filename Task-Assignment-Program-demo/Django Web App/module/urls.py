from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary, name='summary'),
    path('', views.newtask, name='newtask'),
    path('addTask/', views.addTask, name='addTask'),
    path('addCounter/', views.addCounter, name='addCounter'),
    path('newCounter/', views.newCounter, name='newCounter'),
]
