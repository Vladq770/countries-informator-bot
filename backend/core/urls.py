from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('city/<str:name>/', views.get_city, name='GetCity'),
    path('country/<str:name>/', views.get_country, name='GetCountry'),
    path('weather/<str:latitude>/<str:longitude>/', views.get_weather, name='GetWeather'),
    path('currency/<str:code>/', views.get_currency, name='GetCurrency'),
]
