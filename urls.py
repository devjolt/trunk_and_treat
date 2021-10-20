from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='trunk'),
    path('confirmation/', views.confirmation, name='confirmation'),
]