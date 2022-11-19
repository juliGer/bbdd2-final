from rest_framework import serializers
from .models import FlightPrice


class FlightPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightPrice
        fields = '__all__'


class ExecutionTimeSerializer(serializers.Serializer):
    time_sql = serializers.CharField()
    time_no_sql = serializers.CharField()
