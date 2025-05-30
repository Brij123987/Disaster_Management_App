from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_system.serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

import logging
import logging.config
from django.conf import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


@api_view(['POST'])
def create_user(request):
    try:
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({"message":"User Register Successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return Response({"error": "Error creating user"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def user_login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
                "username": username

            }, status=status.HTTP_200_OK)
        

        return Response({"error":"Invalid Uername or Password"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        logger.error(f"Error logging in user: {str(e)}")
        return Response({"error": "Error logging in user"}, status=status.HTTP_400_BAD_REQUEST)