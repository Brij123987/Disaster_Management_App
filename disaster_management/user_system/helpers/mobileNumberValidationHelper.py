import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')

import phonenumbers
from phonenumbers import geocoder, carrier, is_possible_number, is_valid_number
from twilio.rest import Client
from user_system.constant.twilioConfig import TWILIOCONFIG, EARTHQUAKE_MSG, CYCLONE_MSG, VONAGE

import vonage



def google_validate_mobile_number(number):
    try:

        parsed = phonenumbers.parse(number, None)

        phoneData = {
            'possible': is_possible_number(parsed),
            'valid': is_valid_number(parsed),
            'carrier': carrier.name_for_number(parsed, 'en'),
            'region' : geocoder.description_for_number(parsed, 'en'),
        }

        return phoneData
    
    except Exception as e:
        logger.error(f"Error validating mobile number: {str(e)}")
        return False
    

def send_alert_msg_twilio(to_number, alert, magnitude, windSpeed, location):
    print("Sending --------------------------")
    try:
        account_sid = TWILIOCONFIG['account_sid']
        auth_token = TWILIOCONFIG['auth_token']
        fromNum = TWILIOCONFIG['twilio_number']

        print("Msg --------------------------")
        if alert == 'earthquake':
            msg = EARTHQUAKE_MSG.replace("magnitude", magnitude).replace("location", location)
        else:    
            msg = CYCLONE_MSG.replace("windSpeed", "windSpeed").replace("location", location)

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=msg,
            from_=fromNum,
            to=to_number
        )
        print("Message Sent")
        print(f"-----------------------100: {message.sid}")
        return message.sid

    except Exception as e:
        logger.error(f"Error sending alert message: {str(e)}")
        return False
    

def send_alert_msg_vonage(to_number, alert, magnitude, windSpeed, location):
    try:
        client = vonage.Client(key=VONAGE["key"], secret=VONAGE["secret"])
        sms = vonage.Sms(client)

        EARTHQUAKE_MSG = "⚠️ Earthquake Alert: Magnitude magnitude detected near location. Stay safe!"
        CYCLONE_MSG = "🌪️ Cyclone Alert: Wind speed windSpeed km/h expected near location. Take precautions!"

        if alert == 'earthquake':
            msg = EARTHQUAKE_MSG.replace("magnitude", str(magnitude)).replace("location", location)
        else:
            msg = CYCLONE_MSG.replace("windSpeed", str("windSpeed")).replace("location", location)

        response = sms.send_message({
            "from": VONAGE['from'],
            "to": +918452015261,
            "text": msg
        })

        print(response)

        if response["messages"][0]["status"] == "0":
            print("✅ Message sent successfully.")
        else:
            print(f"❌ Message failed: {response['messages'][0]['error-text']}")

    except Exception as e:
        print(f"Error sending alert message: {str(e)}")
        logger.error(f"Error in send_alert_msg_vonage: {str(e)}")