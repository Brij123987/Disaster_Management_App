import logging
import logging.config
import cloudinary.uploader
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


def upload_satelite_image_cloudinary(img_data, image_public_id):
    try:
        result = cloudinary.uploader.upload(
            img_data, 
            public_id=image_public_id,
            folder = 'satellite_image',
            resource_type='image',
            overwrite=True
            )

        return result['secure_url']

    except Exception as e:
        logger.error(f"Error saving satellite image: {str(e)}", exc_info=True)
        return None