import os
from dotenv import load_dotenv

load_dotenv()

import tensorflow as tf
import keras

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import joblib

BASE_DIR = os.getenv('BASE_DIR')

BASE_PATH_CYCLONE_DATA = os.getenv('BASE_PATH_CYCLONE_DATA')
PREDICT_CYCLONE_MODEL = os.path.join(BASE_DIR, 'predict_cyclone_model.h5')


import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


def trained_cyclone_model_data():
    try:
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            BASE_PATH_CYCLONE_DATA,
            validation_split = 0.2,
            subset = 'training',
            seed = 123,
            image_size = (128, 128),
            batch_size = 32
        )

        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            BASE_PATH_CYCLONE_DATA,
            validation_split = 0.2,
            subset = 'validation',
            seed = 123,
            image_size = (128, 128),
            batch_size = 32
        )

        # Prefetch for performance
        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

        cyclone_model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(64, activation='relu'),
            Dense(1, activation='sigmoid')
        ])

        cyclone_model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )


        cyclone_model.fit(train_ds, validation_data = val_ds, epochs = 10)

        # Save the model Data
        logger.error("Model trained and saved successfully.")
        cyclone_model.save(PREDICT_CYCLONE_MODEL)

        return True

    except Exception as e:
        logger.error(f"Error in the trained_cyclone_model_data: {str(e)}", exc_info=True)
        return None