import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("base_dir", BASE_DIR)
BOUNDARIES_JSON_DIR = os.path.join(BASE_DIR, "PB2002_boundaries.json")

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')


def get_boundary_plate_distance(long, lat):
    try:
        boundaries = gpd.read_file(BOUNDARIES_JSON_DIR)

        # Your point of interest
        point = Point(long, lat)

        # Convert to GeoSeries for spatial operations
        point_gdf = gpd.GeoSeries([point], crs="EPSG:4326")

        # Reproject for distance calculation (meters)
        boundaries = boundaries.to_crs(epsg=3857)
        point_gdf = point_gdf.to_crs(epsg=3857)

        # Calculate distance to nearest boundary
        min_distance = boundaries.distance(point_gdf[0]).min()
        
        return min_distance

    except Exception as e:
        logger.error(f"Error in get_boundary_plate_distance: {str(e)}", exc_info=True)
        return None
    

def updated_csv(long, lat, loc):
    try:
        file_path = f"media/earthquake_csv/{loc}_earthquake_data.csv"
        full_path = os.path.join(BASE_DIR, file_path)

        df = pd.read_csv(full_path)

        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df = df.sort_values(by='DateTime')

        df['TimeToNext'] = df['DateTime'].shift(-1) - df['DateTime']
        df['TimeToNext'] = df['TimeToNext'].dt.total_seconds() / 3600


        df['TimeSeriesLast'] = df['DateTime'].diff().dt.total_seconds() / 3600
        df['MagnitudeRollingAvg'] = df['Magnitude'].rolling(window=5).mean()

        df['MagnitudeShifted'] = df['Magnitude'].shift(-1)

        plate_dist = get_boundary_plate_distance(long, lat) / 1000

        df['PlateDistance'] = plate_dist

        return df

    except Exception as e:
        logger.error(f"Error in updated_csv: {str(e)}",exc_info=True)
        return None
