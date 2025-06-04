from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from .ml_processing import model_processing
import pandas as pd
import joblib
import numpy as np
import os

from mlmodel_earthquake.helpers.get_boundary_plate import updated_csv

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.getenv('BASE_DIR')

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

PREDICT_MODEL_PATH = os.path.join(BASE_DIR, "predict_model.pkl")


def train_save_model(location):
    try:
        model = RandomForestClassifier()

        X_train, X_test, y_train, y_test, scaler = model_processing(location)

        if any(x is None for x in [X_train, X_test, y_train, y_test, scaler]):
            logger.error("Data is not available for training the model")
            return False
        
        model.fit(X_train, y_train)

        # Save model and Scaler

        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)

        return True

    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return False



def load_model(input_data, location):
    try:
        res = train_save_model(location)
        if not res:
            logger.error("Model is not trained")
            return None

        model: RandomForestClassifier = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)

        input_array = np.array(input_data)
        if len(input_array.shape) == 1:
            input_array = input_array.reshape(1, -1)

        
        input_scaled = scaler.transform(input_array)

        # input_data [magnitude, depth, lat, long]
        res = model.predict(input_scaled)

        if res is None:
            logger.error("Model prediction failed")
            return None

        return res

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return None


def train_model_predict_next_eartquake():
    try:
        # Load data from DataFrame
        df = updated_csv()

        X = df[['Magnitude', 'Depth', 'TimeSeriesLast', 'PlateDistance']]
        y = df['MagnitudeShifted']

        # Pipeline with scaling and regression
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor())
        ])

        model.fit(X, y)

        # Save Predicted Model
        joblib.dump(model, PREDICT_MODEL_PATH)

        return True
        
    except Exception as e:
        logger.error(f"train_model_predict_next_eartquake: {str(e)}")
        return None
    

def train_model_predict_next_eartquake_with_custom_model(input_data):
    try:
        res = train_model_predict_next_eartquake()

        if not res:
            logger.error("Predicted Model is not available")
            return None
        
        model: RandomForestRegressor = joblib.load(PREDICT_MODEL_PATH)

        input_data = [[5.2, 60.0, 24.5, 10.0]]  # Magnitude, Depth, HoursSinceLast, PlateDistance (km)
        predicted_magnitude = model.predict(input_data)

        print(f"--------------100: {predicted_magnitude[0]:.1f}")

        return f"{predicted_magnitude[0]:.1f}"
    
    except Exception as e:
        logger.error(f"train_model_predict_next_eartquake_with_custom_model: {str(e)}")
        return None