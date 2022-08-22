from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:name>/', views.get_city_country, name='GetCityCountry'),
    path('weather/<str:latitude>/<str:longitude>/', views.get_weather, name='GetWeather'),
    path('currency/<str:code>/', views.get_currency, name='GetCurrency'),
]
