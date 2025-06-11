from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.getenv('BASE_DIR')

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


def train_cyclone_model(location, lat, lon, wind_speed, wind_pressure):
    try:
        # Create a DataFrame from the input data
        file_path = os.path.join(BASE_DIR, "media", "cyclone_csv", f"{location}_cyclone_data.csv")
        df = pd.read_csv(file_path)

        df = df.dropna()

        X = df[['Latitude', 'Longitude', 'windPressure', 'windSpeed']]
        y = df['Storm Develops']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        clf = RandomForestClassifier()
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)


        new_data = [[lat, lon, wind_speed, wind_pressure]]  # Sample values lat, lon, windspeed, windpressure
        prediction = clf.predict(new_data)

        if prediction[0] == 1:
            return "Cyclone is likely to develop in this region."

        else:
            return "No cyclone is expected in this region."

    except Exception as e:
        logger.error(f"Error in the train_cyclone_model function: {str(e)}", exc_info=True)
        return None
