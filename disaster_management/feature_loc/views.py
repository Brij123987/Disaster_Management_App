from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from feature_loc.helpers.get_user_locations import get_location_coordinates
from feature_loc.helpers.earthquake_data_write import write_earthquake_data_to_csv
import requests
import os

from mlmodel_earthquake.training_model import load_model

from dotenv import load_dotenv
load_dotenv()

EARTHQUAKE_HISTORICAL_DATA = os.getenv('EARTHQUAKE_HISTORICAL_URLS')

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')



# Create your views here.

@api_view(['GET'])
def get_location_earthquake_historical_data(request):
    try:
        location = request.query_params.get('location')

        if not location:
            return Response({'error': 'Location is required'}, status=status.HTTP_400_BAD_REQUEST)

        urls = EARTHQUAKE_HISTORICAL_DATA

        lat, lon = get_location_coordinates(location)
        print(lat, lon)

        if not lat or not lon:
            return Response({'error': 'Unable to get location'}, status=status.HTTP_400_BAD_REQUEST)

        params = {
            'format': 'geojson',
            'latitude': lat,
            'longitude': lon,
            'maxradiuskm': 1000,
            'starttime': '2025-05-01',
            'endtime': '2025-05-31',
        }

        response = requests.get(urls, params=params)

        if response.status_code != 200:
            return Response({'error': 'Unable to get data'}, status=status.HTTP_400_BAD_REQUEST)

        data = response.json()

        if not data or not data['features']:
            return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        


        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']

            csv_data = write_earthquake_data_to_csv(location, props, coords)

            if not csv_data:
                return Response({'error': 'Unable to write data to csv'}, status=status.HTTP_400_BAD_REQUEST)

        data_send = [[props['mag'], coords[2], coords[1], coords[0]]]
        predicted_data = load_model(data_send)

        if not predicted_data:
            return Response({'error': 'Unable to predict data'}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'location': location,
            'latitude': lat,
            'longitude': lon,
            'Magnitude' : props['mag'],
            'coords': coords,
            'predicted_data': predicted_data
        }

        return Response({'data':response_data}, status=status.HTTP_200_OK)


    except Exception as e:
        logger.error(f"Error in get_location_earthquake_historical_data: {str(e)}")
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
