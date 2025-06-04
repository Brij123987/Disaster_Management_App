import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from dotenv import load_dotenv
load_dotenv()

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


BASE_DIR = os.getenv('BASE_DIR')




def model_processing(location):
    try:
        # EarthQuake DataSet
        file_path = f"{location}_earthquake_data.csv"
        full_path = os.path.join(BASE_DIR, file_path)

        df = pd.read_csv(full_path)
        
        if df.empty:
            logger.error("The data frame is empty")
            return None

        # Drop Duplicate Value 
        df.drop_duplicates(inplace=True)

        # Feature Selection
        X = df[['Magnitude','Depth','Latitude','Longitude']]
        y = df['AfterShock_Risk']

        # Scaling Features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

        return X_train, X_test, y_train, y_test, scaler
    
    except Exception as e:
        logger.error(f"Error in model processing: {str(e)}")
        return None, None, None, None
