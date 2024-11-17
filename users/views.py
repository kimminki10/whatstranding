from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from .models import User
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.core.cache import cache
from django.urls import reverse
from django.conf import settings
import uuid

def send_verification_email(request, email):
    # Generate token
    token = str(uuid.uuid4())
    cache.set(token, email, timeout=300)  # 5 minutes

    # Send email
    verification_link = request.build_absolute_uri(reverse('verify-email', args=[token]))
    send_mail(
        'Verify your email',
        f'Click the link to verify your email: {verification_link}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        send_verification_email(request, user.email)
        return response
    
class EmailVerification(APIView):
    def get(self, request, token):
        email = cache.get(token)
        if email:
            cache.delete(token)
            user = User.objects.get(email=email)
            user.is_email_verified = True
            user.save()
            return Response({'message': 'Email verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes([permissions.IsAuthenticated])
    def post(self, request, token):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            if user.is_email_verified:
                return Response({'message': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
            
            send_verification_email(request, email)
            return Response({'message': 'Verification email sent'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)