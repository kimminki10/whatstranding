from django.urls import path
from .views import UserListCreate, EmailVerification

urlpatterns = [
    path('', UserListCreate.as_view(), name='user-list-create'),
    path('verify-email/<str:token>/', EmailVerification.as_view(), name='verify-email'),
]