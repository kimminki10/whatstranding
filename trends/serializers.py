from rest_framework import serializers
from .models import Trend

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'name', 'description', 'search_volume', 'started_at','created_at', 'updated_at')

