import base64
from io import BytesIO
from tkinter import Image
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from feature_loc.helpers.get_user_locations import get_location_coordinates
from feature_loc.helpers.earthquake_data_write import write_earthquake_data_to_csv, convert_even_time_to_datetime
import requests
import os
from datetime import datetime, timezone

from mlmodel_earthquake.training_model import load_model, train_model_predict_next_eartquake_with_custom_model
from mlmodel_earthquake.helpers.get_boundary_plate import get_boundary_plate_distance
from feature_loc.helpers.convert_loc_into_bbox_helpers import get_bbox
from feature_loc.helpers.generate_sateliite_img_helpers import generate_satellite_img_of_location
from feature_loc.helpers.cyclone_data_sourcing_helpers import get_cyclone_detail_data
from feature_loc.helpers.save_satellite_img_helpers import upload_satelite_image_cloudinary

from dotenv import load_dotenv
load_dotenv()

EARTHQUAKE_HISTORICAL_DATA = os.getenv('EARTHQUAKE_HISTORICAL_URLS')

CYCLONE_LOCATION_DATA = os.getenv('CYCLONE_LOCATION_DATA')

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

        if not lat or not lon:
            return Response({'error': 'Unable to get location'}, status=status.HTTP_400_BAD_REQUEST)

        params = {
            'format': 'geojson',
            'latitude': lat,
            'longitude': lon,
            'maxradiuskm': 1000,
            'starttime': '2025-05-01',
            'endtime': '2025-06-11',
        }

        response = requests.get(urls, params=params)

        if response.status_code != 200:
            return Response({'error': 'Unable to get data'}, status=status.HTTP_400_BAD_REQUEST)

        data = response.json()
    
        if not data or not data['features']:
            return Response({'error': 'No data found'}, status=status.HTTP_404_NOT_FOUND)
        
        props = data['features'][0]['properties']
        coords = data['features'][0]['geometry']['coordinates']

        csv_data = write_earthquake_data_to_csv(location, data['features'])

        if not csv_data:
            return Response({'error': 'Unable to write data to csv'}, status=status.HTTP_400_BAD_REQUEST)

        plate_distance = get_boundary_plate_distance(coords[0], coords[1]) / 1000

        if not plate_distance:
            return Response({'error': 'Unable to get plate distance'}, status=status.HTTP_400_BAD_REQUEST)
        
        data_send = [[props['mag'], coords[2], coords[1], coords[0], props['time'] / 3600, plate_distance]]
        predicted_data = load_model(data_send, coords[0], coords[1], location)

        if not predicted_data:
            return Response({'error': 'Unable to predict data'}, status=status.HTTP_400_BAD_REQUEST)

        predict_next_earthquake = train_model_predict_next_eartquake_with_custom_model(props['mag'], coords[2], props['time'], plate_distance, coords[0], coords[1], location)

        response_data = {
            'location': location,
            'latitude': lat,
            'longitude': lon,
            'Magnitude' : props['mag'],
            'coords': coords,
            'predicted_data': predicted_data,
            'predict_next_earthquake': predict_next_earthquake
        }

        return Response({'data':response_data}, status=status.HTTP_200_OK)


    except Exception as e:
        logger.error(f"Error in get_location_earthquake_historical_data: {str(e)}", exc_info=True)
        return Response({"error message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cyclone_prediction(request):
    try:
        location = request.query_params.get('location')

        if not location:
            return Response({'error': 'Location is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        lat, lon = get_location_coordinates(location)

        if not lat or not lon:
            return Response({'error': 'Location not found'}, status=status.HTTP_400_BAD_REQUEST)

        minx, miny, maxx, maxy = get_bbox(lon, lat)

        if not all([minx, miny, maxx, maxy]):
            return Response({'error': 'Unable to get bbox'}, status=status.HTTP_400_BAD_REQUEST)

        response = generate_satellite_img_of_location(minx, miny, maxx, maxy)
        
        if response.status_code != 200:
            return Response({'error': 'Unable to get cyclone data'}, status=status.HTTP_400_BAD_REQUEST)
        
        cyclone_data = get_cyclone_detail_data(lat, lon)

        if not cyclone_data:
            return Response({'error': 'Unable to get cyclone data'}, status=status.HTTP_400_BAD_REQUEST)

        image_url = upload_satelite_image_cloudinary(response.content, location)

        if not image_url:
            return Response({'error': 'Unable to upload image'}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'location': location,
            'image_url': image_url,
            'cyclone_data': cyclone_data
        }
        
        # return HttpResponse(response.content, content_type="image/png", status=status.HTTP_200_OK, headers={"Content-Disposition": "attachment; filename=satellite.png"})

        return Response({'data':response_data}, status=status.HTTP_200_OK)


    except Exception as e:
        logger.error(f"Error in get_cyclone_prediction: {str(e)}", exc_info=True)
        return Response({"error message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
