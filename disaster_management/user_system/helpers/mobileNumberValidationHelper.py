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


def twilio_number_verification(phone_number):
    try:
        client = Client(TWILIOCONFIG['account_sid'], TWILIOCONFIG['auth_token'])

        verification = (
            client.verify
            .services(TWILIOCONFIG['verify_service_sid'])
            .verifications
            .create(to=phone_number, channel="sms")
        )


        return verification.status

    except Exception as e:
        logger.error(f"Error validating mobile number: {str(e)}")
        return False
    
def twilio_number_verification_status(phone_number, code):
    try:
        client = Client(TWILIOCONFIG['account_sid'], TWILIOCONFIG['auth_token'])

        verification_check = (
            client.verify
            .services(TWILIOCONFIG['verify_service_sid'])
            .verification_checks
            .create(to=phone_number, code=code)
        )

        if verification_check.status == 'approved':
            return True
        else:
            return False

    except Exception as e:
        logger.error(f"Error validating mobile number: {str(e)}")
        return False

def send_alert_msg_twilio(to_number, alert, magnitude, windSpeed, location):
    try:
        account_sid = TWILIOCONFIG['account_sid']
        auth_token = TWILIOCONFIG['auth_token']
        fromNum = TWILIOCONFIG['twilio_number']

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

        return message.sid

    except Exception as e:
        logger.error(f"Error sending alert message: {str(e)}")
        return False
    