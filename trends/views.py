from rest_framework import generics
from .models import Trend
from .serializers import TrendSerializer

class TrendListCreateView(generics.ListCreateAPIView):
    queryset = Trend.objects.all()
    serializer_class = TrendSerializer


class TrendDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trend.objects.all()
    serializer_class = TrendSerializer