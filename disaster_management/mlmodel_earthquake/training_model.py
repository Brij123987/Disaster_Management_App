from sklearn.ensemble import RandomForestClassifier
from .ml_processing import model_processing
import joblib

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

def train_save_model():
    try:
        model = RandomForestClassifier()

        X_train, X_test, y_train, y_test, scaler = model_processing()

        if not all([X_train, X_test, y_train, y_test, scaler]):
            logger.error("Data is not available for training the model")
            return False
        
        model.fit(X_train, y_train)

        # Save model and Scaler

        joblib.dump(model, "model.pkl")
        joblib.dump(scaler, "scaler.pkl")

        return True

    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return False
    

def load_model(input_data):
    try:
        model: RandomForestClassifier = joblib.load("model.pkl")

        res = model.predict(input_data)

        if res is None:
            logger.error("Model prediction failed")
            return None

        return res

    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return None

