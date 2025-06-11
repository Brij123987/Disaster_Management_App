
from datetime import datetime, timedelta


import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

def get_start_date(current_date):
    try:
        current_date = datetime.strptime(current_date, '%Y-%m-%d')

        start_date = current_date - timedelta(days=30)

        if not start_date:
            logger.error(f"Error in getting the End Date:")

        return start_date.strftime('%Y-%m-%d')
    

    except Exception as e:
        logger.error(f"Error in get_start_date function: {str(e)}", exc_info=True)
        return None