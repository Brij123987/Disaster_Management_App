import os 
import csv

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

def write_earthquake_data_to_csv(location, prop, coord):
    try:
        file_path = f'{location}_earthquake_data.csv'

        header = ['Magnitude', 'Depth', 'Latitude', 'Longitude', 'AfterShock_Risk']

        file_exists = os.path.isfile(file_path)
        file_empty = not file_exists or os.stat(file_path).st_size == 0

        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            if file_empty:
                writer.writerow(header)
            
            writer.writerow(
                [
                    prop['mag'],
                    coord[2],
                    coord[1],
                    coord[0],
                    "N/A"
                ]
            )

            return True

    except Exception as e:
        logger.error(f"Error in the function write_earthquake_data_to_csv: {e}")
        return False

