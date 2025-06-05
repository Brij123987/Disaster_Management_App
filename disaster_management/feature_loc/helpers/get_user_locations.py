from geopy.geocoders import Nominatim


import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

def get_location_coordinates(location):
    try:
        geolocator = Nominatim(user_agent="my_user_agent")
        location = geolocator.geocode(location)

        if location is not None:
            return location.latitude, location.longitude
        
        else:
            return None, None
        
    except Exception as e:
        logger.error(f"Error getting location coordinates: {str(e)}", exc_info=True)
        return None, None