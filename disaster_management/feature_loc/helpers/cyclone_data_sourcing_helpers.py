import os
from dotenv import load_dotenv
load_dotenv()

import requests

CYCLONE_DETAILS_DATA_URL = os.getenv('CYCLONE_DETAILS_DATA_URL')
CYCLONE_DATA_API_KEY = os.getenv('CYCLONE_DATA_API_KEY')

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


def get_cyclone_detail_data(latitude, longitude):
    try:
        urls = CYCLONE_DETAILS_DATA_URL

        params = {
            'lat' : latitude,
            'lon' : longitude,
            'appid' : CYCLONE_DATA_API_KEY
        }

        response = requests.get(urls, params=params)

        if response.status_code != 200:
            logger.error(f"Failed to retrieve cyclone data. Status code: {response.status_code}")
            return None
        
        return response.json()


    except Exception as e:
        logger.error(f"Error occurred while fetching cyclone detail data: {str(e)}", exc_info=True)
        return None