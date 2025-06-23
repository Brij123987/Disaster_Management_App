import os
import requests
from datetime import datetime, timedelta

CYCLONE_LOCATION_DATA = os.getenv('CYCLONE_LOCATION_DATA')

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')



def generate_satellite_img_of_location(minx, miny, maxx, maxy, current_date):
    try:
        current_date_str = datetime.now().strftime('%Y-%m-%d')
        print("Current date:", current_date_str)

        # Convert string to datetime and subtract 1 day
        date_obj = datetime.strptime(current_date_str, '%Y-%m-%d')
        previous_date_obj = date_obj - timedelta(days=1)

        # Convert back to string
        previous_date_str = previous_date_obj.strftime('%Y-%m-%d')
        
        urls = CYCLONE_LOCATION_DATA
    
        params = {
            "SERVICE" : "WMS",
            "VERSION" : "1.3.0",
            "WIDTH" : "2048",
            "HEIGHT" : "512",
            "LAYERS" : "MODIS_Terra_CorrectedReflectance_TrueColor",
            "FORMAT" : "image/png",
            "REQUEST" : "GetMap",
            "TIME" : previous_date_str,
            "CRS" : "EPSG:3857",
            "BBOX" : f"{minx}, {miny}, {maxx}, {maxy}",
            "TRANSPARENT" : "TRUE"
        }

        response = requests.get(urls, params = params)

        return response

    except Exception as e:
        logger.error(f"Error generating satellite image of location: {str(e)}", exc_info=True)
        return None