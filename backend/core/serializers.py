from rest_framework import serializers
from .models import Country, City


class WeatherSerializer(serializers.Serializer):
    temp = serializers.FloatField()
    feels_like = serializers.FloatField()
    condition = serializers.CharField(max_length=100)
    wind_speed = serializers.FloatField()
    wind_gust = serializers.FloatField()
    wind_dir = serializers.CharField(max_length=4)
    pressure_mm = serializers.FloatField()
    humidity = serializers.FloatField()


class CurrencySerializer(serializers.Serializer):
    Nominal = serializers.FloatField()
    Value = serializers.FloatField()
    Name = serializers.CharField(max_length=20)
    CharCode = serializers.CharField(max_length=4)


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        exclude = ["country", "created_at"]


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        exclude = ["created_at"]

