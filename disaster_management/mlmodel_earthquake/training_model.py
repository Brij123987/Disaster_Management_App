from sklearn.ensemble import RandomForestClassifier
from .ml_processing import model_processing
import joblib
import numpy as np
import os

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


def train_save_model():
    try:
        model = RandomForestClassifier()

        X_train, X_test, y_train, y_test, scaler = model_processing()

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



def load_model(input_data):
    try:
        train_save_model()

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

