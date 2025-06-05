from datetime import datetime, timezone
from mlmodel_earthquake.helpers.get_boundary_plate import updated_csv

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

def get_time_since_last_earthquake(event_time, long, lat, loc):
    try:
        curr_time = datetime.fromtimestamp(event_time, tz=timezone.utc)

        data = updated_csv(long, lat, loc)
        last_earthquake_time = data['DateTime'].iloc[0].replace(tzinfo=timezone.utc)
        print(f"-------------100: {last_earthquake_time}")
    
        time_since_last = (curr_time - last_earthquake_time).total_seconds() / 3600
        print(f"-------------------200: {time_since_last}")

        return time_since_last
    
    except Exception as e:
        logger.error(f"Error in get_time_since_last_earthquake: {str(e)}", exc_info=True)
        return None
