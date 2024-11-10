from django.urls import path
from . import views

urlpatterns = [
    path('', views.TrendListCreateView.as_view(), name='trend-list-create'),
    path('<int:pk>/', views.TrendDetailView.as_view(), name='trend-detail'),
]

