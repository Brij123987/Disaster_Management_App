from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_system.serializers import RedisUserSerializer
from user_system.redis_store import RedisUserData
import json

import uuid

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

# Create your views here.

@api_view(['GET'])
def get_user_data(request):
    try:
        user_id = request.query_params.get('user_id')
    
        redis_handler = RedisUserData()
        user_data = redis_handler.get_user_data(user_id)

        if user_data is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = json.loads(user_data)

        serializer = RedisUserSerializer({"user_id":user_id, "data":data})

        return Response(serializer.data, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        logger.error('Error decoding JSON')
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f'Error getting user data: {e}', exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def create_user_data(request):
    try:
        user_id = str(uuid.uuid4())
        data = request.data.copy()
        data['user_id'] = user_id
        serializer = RedisUserSerializer(data=data)

        if serializer.is_valid(): 
            user_data = serializer.validated_data['data']

            redis_handler = RedisUserData()
            redis_handler.set_user_data(user_id, json.dumps(user_data))

            return Response({"message":"User Created Successfully", "user_id":user_id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    except Exception as e:
        logger.error(f'Error creating user data: {e}', exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    