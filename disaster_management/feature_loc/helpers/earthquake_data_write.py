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
        logger.error(f"Error in estimate_aftershock_risk: {str(e)}", exc_info=True)
        return None


def convert_even_time_to_datetime(Event_time):
    try:
        # Convert Event time to datetime format
        event_time = datetime.fromtimestamp(Event_time / 1000.0)
        event_time = event_time.strftime('%Y-%m-%d %H:%M:%S')

        return event_time
  
    except Exception as e:
        logger.error(f"Error in convert_even_time_to_datetime: {str(e)}", exc_info=True)
        return None



def write_earthquake_data_to_csv(location, features):
    try:
        file_path = f'media/earthquake_csv/{location}_earthquake_data.csv'
        header = ['ID', 'DateTime', 'Magnitude', 'Depth', 'Latitude', 'Longitude', 'AfterShock_Risk']

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
        for feature in features:
            prop = feature['properties']
            coord = feature['geometry']['coordinates']
            event_time = convert_even_time_to_datetime(prop['time'])
            if not event_time:
                continue

            event_id = prop.get('id') or f"{event_time}_{coord[1]}_{coord[0]}"
            if event_id in existing_ids:
                continue

            aftershock_risk = estimate_aftershock_risk(prop['mag'], coord[2], event_time)
            if not aftershock_risk:
                aftershock_risk = 'N/A'

            new_rows.append([
                event_id,
                event_time,
                prop['mag'],
                coord[2],
                coord[1],
                coord[0],
                aftershock_risk
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
        logger.error(f"Error in the function write_earthquake_data_to_csv: {e}",exc_info=True)
        return False

