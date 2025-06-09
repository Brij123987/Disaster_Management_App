from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


def train_cyclone_model(lat, lon, wind_speed, pressure, storm_develops):
    try:
        
        # Create a DataFrame from the input data
        X = pd.DataFrame({'latitude': lat, 'longitude': lon, 'wind_speed': wind_speed, 'pressure': pressure, "storm_develops": storm_develops})
        pass



    except Exception as e:
        logger.error(f"Error in the train_cyclone_model function: {str(e)}", exc_info=True)
        return None, None