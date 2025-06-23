from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from .ml_processing import model_processing
from sklearn.metrics import mean_absolute_error, accuracy_score
import pandas as pd
import joblib
import numpy as np
import os

from mlmodel_earthquake.helpers.calculate_time_difference_helpers import get_time_since_last_earthquake
from mlmodel_earthquake.helpers.get_boundary_plate import updated_csv

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
PREDICT_MODEL_PATH = os.path.join(BASE_DIR, "predict_model.pkl")
PREDICT_MODEL_TIME_PATH = os.path.join(BASE_DIR, "predict_model_time.pkl")


def train_save_model(long, lat, location):
    try:
        model = RandomForestClassifier()

        X_train, X_test, y_train, y_test, scaler = model_processing(long, lat, location)

        if any(x is None for x in [X_train, X_test, y_train, y_test, scaler]):
            logger.error("Data is not available for training the model")
            return False
        
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc =  accuracy_score(y_test, y_pred)
        logger.error(f"Classifier Accuracy: {acc:.4f}")

        # Save model and Scaler
        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)

        return True

    except Exception as e:
        logger.error(f"Error training model: {str(e)}" , exc_info=True)
        return False



def load_model(input_data, long, lat, location):
    try:
        res = train_save_model(long, lat, location)
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
        logger.error(f"Error loading model: {str(e)}", exc_info=True)
        return None


def train_model_predict_next_eartquake(long, lat, loc):
    try:
        # Load data from DataFrame
        df = updated_csv(long, lat, loc)

        df = df.dropna(subset=['MagnitudeShifted'])

        X = df[['Magnitude', 'Depth', 'TimeSeriesLast', 'PlateDistance']]
        y = df['MagnitudeShifted']

        # Pipeline with scaling and regression
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor())
        ])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)

        # 🔍 Evaluate MAE
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        logger.error(f"Magnitude Prediction MAE: {mae:.2f}")

        # Save Predicted Model
        joblib.dump(model, PREDICT_MODEL_PATH)

        return True
        
    except Exception as e:
        logger.error(f"train_model_predict_next_eartquake: {str(e)}", exc_info=True)
        return None
    

def train_model_predict_next_eartquake_time(long, lat, loc):
    try:
        df = updated_csv(long, lat, loc)

        df = df.dropna(subset=['TimeToNext'])

        X = df[['Magnitude', 'Depth', 'TimeSeriesLast', 'PlateDistance']]
        y = df['TimeToNext']

        # Pipeline with scaling and regression
        model_time = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', RandomForestRegressor())
        ])

        
        model_time.fit(X, y)

        # Save Predicted Model
        joblib.dump(model_time, PREDICT_MODEL_TIME_PATH)

        return True

    except Exception as e:
        logger.error(f"train_model_predict_next_eartquake_time: {str(e)}", exc_info=True)
        return None
    

def train_model_predict_next_eartquake_with_custom_model(magnitude, depth, event_time, plate_distance, long, lat, loc):
    try:
        res = train_model_predict_next_eartquake(long, lat, loc)
        res_1 = train_model_predict_next_eartquake_time(long, lat, loc)

        if not res or not res_1:
            logger.error("Predicted Model is not available")
            return None
        
        model: RandomForestRegressor = joblib.load(PREDICT_MODEL_PATH)
        model_time: RandomForestRegressor = joblib.load(PREDICT_MODEL_TIME_PATH)

        # time_since_last = get_time_since_last_earthquake(event_time, long, lat, loc)

        # if not time_since_last:
        #     logger.error("Time since last earthquake is not available")

        input_data = [[magnitude, depth, event_time, plate_distance]]
       
        predicted_magnitude = model.predict(input_data)
        predicted_time = model_time.predict(input_data)



        return {
            "PredictedMagnitude": round(predicted_magnitude[0], 1),
            "ExpectedInHours": abs(round(predicted_time[0], 1))
        }
    
    except Exception as e:
        logger.error(f"train_model_predict_next_eartquake_with_custom_model: {str(e)}", exc_info=True)
        return None