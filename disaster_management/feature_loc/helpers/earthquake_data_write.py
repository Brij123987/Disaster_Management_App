import os 
import csv
from datetime import datetime, timezone



import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

def estimate_aftershock_risk(magnitude, depth_km, event_time):
    try:
        
        if magnitude < 2.5:
            return 'Low'
        
        event_time = datetime.fromisoformat(event_time)
        event_time = event_time.replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)
        days_since_event = (current_time - event_time).days

        if magnitude >= 6.5:
            dacay_period = 60
        elif magnitude >= 5.0:
            dacay_period = 30
        else:
            dacay_period = 10

        risk_score = max(0, 1.0 - (days_since_event / dacay_period))

        if risk_score > 0.7:
            return 'High'
        elif risk_score > 0.3:
            return 'Medium'
        else:
            return 'Low'
        

    except Exception as e:
        logger.error(f"Error in estimate_aftershock_risk: {str(e)}")
        return None


def convert_even_time_to_datetime(Event_time):
    try:
        # Convert Event time to datetime format
        event_time = datetime.fromtimestamp(Event_time / 1000.0)
        event_time = event_time.strftime('%Y-%m-%d %H:%M:%S')

        return event_time
  
    except Exception as e:
        logger.error(f"Error in convert_even_time_to_datetime: {str(e)}")
        return None



def write_earthquake_data_to_csv(location, prop, coord):
    try:
        file_path = f'{location}_earthquake_data.csv'

        header = ['DateTime','Magnitude', 'Depth', 'Latitude', 'Longitude', 'AfterShock_Risk']

        file_exists = os.path.isfile(file_path)
        file_empty = not file_exists or os.stat(file_path).st_size == 0

        event_time = convert_even_time_to_datetime(prop['time'])

        if not event_time:
            logger.error(f"Error in write_earthquake_data_to_csv: {str(e)}")
            return None

        aftershock_risk = estimate_aftershock_risk(prop['mag'], coord[2], event_time)
        # print(f"------------------100: {aftershock_risk}")

        if not aftershock_risk:
            return 'N/A'

        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            if file_empty:
                writer.writerow(header)
            
            writer.writerow(
                [
                    event_time,
                    prop['mag'],
                    coord[2],
                    coord[1],
                    coord[0],
                    aftershock_risk
                ]
            )

            return True

    except Exception as e:
        logger.error(f"Error in the function write_earthquake_data_to_csv: {e}")
        return False

