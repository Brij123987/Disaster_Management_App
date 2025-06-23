import pandas as pd
import os
from pathlib import Path


from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


def get_eathquake_data_from_csv(location):
    try:
        file_name = f"/media/earthquake_csv/{location}_earthquake_data.csv"

        file_path = BASE_DIR + file_name


        df = pd.read_csv(file_path)
        df = df.drop(columns=['ID'])

        earthquake_data = df.to_dict(orient='records')

        return earthquake_data

    except Exception as e:
        logger.error(f"Error in get_eathquake_data_from_csv: {str(e)}", exc_info=True)
        return None
    

def get_cyclone_data_from_csv(location):
    try:
        file_name = f"/media/cyclone_csv/{location}_cyclone_data.csv"

        file_path = BASE_DIR + file_name

        df = pd.read_csv(file_path)
        df = df.drop(columns=['ID'])

        cyclone_data = df.to_dict(orient='records')

        return cyclone_data

    except Exception as e:
        logger.error(f"Error in get_cyclone_data_from_csv: {str(e)}", exc_info=True)
        return None