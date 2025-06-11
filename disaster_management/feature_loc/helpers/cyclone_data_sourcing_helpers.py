import os
import csv
from dotenv import load_dotenv
load_dotenv()

import requests

CYCLONE_DETAILS_DATA_URL = os.getenv('CYCLONE_DETAILS_DATA_URL')
CYCLONE_DATA_API_KEY = os.getenv('CYCLONE_DATA_API_KEY')
CYCLONE_HISTORICAL_DATA_URL = os.getenv('CYCLONE_HISTORICAL_DATA_URL')


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
        
        data = response.json()
        windspeed = data['wind']['speed']
        
        storm_result = get_storm_developes(windspeed) 

        return response.json(), storm_result


    except Exception as e:
        logger.error(f"Error occurred while fetching cyclone detail data: {str(e)}", exc_info=True)
        return None, None
    
def get_cyclone_historical_data(location, latitude, longitude, start_date, end_date):
    try:
        urls = CYCLONE_HISTORICAL_DATA_URL

        params = {
            "latitude" : latitude,
            "longitude" : longitude,
            "start_date" : start_date,
            "end_date" : end_date,
            "daily" : "pressure_msl_max,windspeed_10m_max",
            "timezone" : "auto"
        }
        print(params)

        response = requests.get(urls, params=params)
        print(response)

        if response.status_code != 200:
            logger.error(f"Failed to retrieve cyclone historical data. Status code: {response.status_code}")
            return None
        
        historical_data = response.json()

        csv_data = write_cyclone_daily_data_to_csv(location, historical_data)

        if not csv_data:
            logger.error(f"Failed to write cyclone historical data to csv file")
            return False

        return True

    except Exception as e:
        logger.error(f"Error occurred while fetching cyclone historical data: {str(e)}", exc_info=True)
        return None


def get_storm_developes(windspeed):
    try:
        if not windspeed:
            return None

        if windspeed >= 34:
            return 1
        
        return 0

    except Exception as e:
        logger.error(f"Error occurred while fetching storm develops: {str(e)}", exc_info=True)
        return None


def write_cyclone_daily_data_to_csv(location, response_data):
    try:
        file_path = f'media/cyclone_csv/{location}_cyclone_data.csv'
        header = ['ID', 'Date', 'Latitude', 'Longitude', 'windPressure', 'windSpeed', 'Storm Develops']

        # Step 1: Load existing IDs once
        existing_ids = set()
        file_exists = os.path.isfile(file_path)
        file_empty = not file_exists or os.stat(file_path).st_size == 0

        if file_exists:
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                existing_ids = {row['ID'] for row in reader}

        # Step 2: Prepare new rows in memory
        new_rows = []
        dates = response_data['daily']['time']
        pressures = response_data['daily']['pressure_msl_max']
        windspeeds = response_data['daily']['windspeed_10m_max']
        lat = response_data['latitude']
        lon = response_data['longitude']

        for i in range(len(dates)):
            date = dates[i]
            pressure = pressures[i]
            windspeed = windspeeds[i]

            # Skip data points with null values
            if pressure is None or windspeed is None:
                continue

            # Create a unique ID for this entry
            row_id = f"{location}_{date}"
            if row_id in existing_ids:
                continue

            # Determine if storm develops (example logic: windspeed > 60 km/h)
            storm_develops = get_storm_developes(windspeed)

            new_rows.append([
                row_id,
                date,
                lat,
                lon,
                pressure,
                windspeed,
                storm_develops
            ])

        # Step 3: Write only new rows
        if new_rows:
            with open(file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if file_empty:
                    writer.writerow(header)
                writer.writerows(new_rows)

        return True

    except Exception as e:
        logger.error(f"Error occurred while writing cyclone daily data to csv: {str(e)}", exc_info=True)
        return False