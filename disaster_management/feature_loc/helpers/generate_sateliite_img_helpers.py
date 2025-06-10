import os
import requests


CYCLONE_LOCATION_DATA = os.getenv('CYCLONE_LOCATION_DATA')

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')



def generate_satellite_img_of_location(minx, miny, maxx, maxy):
    try:
        urls = CYCLONE_LOCATION_DATA
    
        params = {
            "SERVICE" : "WMS",
            "VERSION" : "1.3.0",
            "WIDTH" : "2048",
            "HEIGHT" : "512",
            "LAYERS" : "MODIS_Terra_CorrectedReflectance_TrueColor",
            "FORMAT" : "image/png",
            "REQUEST" : "GetMap",
            "TIME" : "2025-06-10",
            "CRS" : "EPSG:3857",
            "BBOX" : f"{minx}, {miny}, {maxx}, {maxy}",
            "TRANSPARENT" : "TRUE"
        }

        response = requests.get(urls, params = params)

        return response

    except Exception as e:
        logger.error(f"Error generating satellite image of location: {str(e)}", exc_info=True)
        return None