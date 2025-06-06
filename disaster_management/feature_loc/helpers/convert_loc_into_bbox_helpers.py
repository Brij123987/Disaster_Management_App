from pyproj import Transformer


import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')



def get_bbox(lon, lat):
    try:
        # Create transformer
        transform = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        x_center, y_center = transform.transform(lon, lat)

        # Expand by 100000 meters (about 1° in Web Mercator)
        delta = 100000

        minx = x_center - delta
        maxx = x_center + delta
        miny = y_center - delta
        maxy = y_center + delta

        return minx, miny, maxx, maxy

    except Exception as e:
        logger.error(f"Error in get_bbox: {e}", exc_info=True)
        return None, None, None, None