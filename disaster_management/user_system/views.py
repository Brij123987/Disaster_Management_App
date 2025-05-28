from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


# Create your views here.

@api_view(['GET'])
def get_user_data(request, user_id):
    try:
        pass
    except Exception as e:
        pass