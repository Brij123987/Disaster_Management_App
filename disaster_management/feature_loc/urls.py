from django.urls import path
from feature_loc import views

app_name = 'feature_loc'

urlpatterns = [
    path('get_location_earthquake_historical_data/', views.get_location_earthquake_historical_data, name='get_location_earthquake_historical_data'),
    path('get_cyclone_prediction/', views.get_cyclone_prediction, name="get_cyclone_prediction"),
]