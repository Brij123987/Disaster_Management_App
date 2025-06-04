from datetime import datetime

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

def get_time_since_last_earthquake(event_time):
    try:
        pass
    except Exception as e:
        logger.error(f"Error in get_time_since_last_earthquake: {str(e)}")
        return None
