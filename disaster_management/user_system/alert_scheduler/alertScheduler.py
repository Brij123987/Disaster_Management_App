import requests
from datetime import datetime

def check_and_send_alerts():
    from user_system.models import UserLocationDetail
    from user_system.helpers.mobileNumberValidationHelper import send_alert_msg_twilio

    print("Starting...............................")
    API_URL = "https://disastermanagementapp-production.up.railway.app"
    date = datetime.today().strftime('%Y-%m-%d')

    try:
        userLocation = UserLocationDetail.objects.filter(isTracked=True).values('location', 'country_code', 'phonenumber')

        for user in userLocation:
            location = user['location']
            phonenumber = user['country_code'] + user['phonenumber']

            earthquake_response = requests.get(
                f'{API_URL}/feature/get_location_earthquake_historical_data/?location={location}&date={date}'
            )

            if earthquake_response.status_code == 200:
                data = earthquake_response.json()
                if data.get('data', {}).get('predicted_data') == "High":
                    magnitude = data.get('data', 0).get('Magnitude')
                    send_alert_msg_twilio(phonenumber, "earthquake", magnitude, windSpeed=None, location=location)

            cyclone_response = requests.get(
                f'{API_URL}/feature/get_cyclone_prediction/?location={location}&end_date={date}'
            )

            if cyclone_response.status_code == 200:
                data = cyclone_response.json()
                if data.get('data', {}).get('CyclonePrediction') == "No cyclone is expected in this region.":
                    print("Cyclone Data Fetch ")
                    send_alert_msg_twilio(phonenumber, "cyclone", windSpeed=None, magnitude=None, location=location)
        
        print("Ended---------------------------------------------")

    except Exception as e:
        print(f"An error occurred during alert scheduling: {e}")



