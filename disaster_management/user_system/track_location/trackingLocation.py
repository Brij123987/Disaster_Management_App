from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from geopy.distance import geodesic
from user_system.models import UserLocationDetail
from user_system.helpers.mobileNumberValidationHelper import google_validate_mobile_number
from user_system.helpers.mobileNumberValidationHelper import twilio_number_verification, twilio_number_verification_status


import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_update_location(request):
    try:
        user = request.user
        location = request.data.get('location')
        lat = request.data.get('lat')
        lon = request.data.get('lon')
        mobileNumber = request.data.get('mobileNumber')
        countryCode = request.data.get('countryCode')
        locationConsent = request.data.get('locationConsent')

        phoneNumber = countryCode + mobileNumber

        phoneData = google_validate_mobile_number(phoneNumber)

        if not phoneData.get('possible') and not phoneData.get('possible'):
            return Response({'error': 'Invalid mobile number'}, status=status.HTTP_200_OK)
    
        # Get or create only based on user
        record, created = UserLocationDetail.objects.get_or_create(user=user)

        # Always update the static fields
        record.phonenumber = mobileNumber
        record.country_code = countryCode
        record.isTracked = locationConsent

        # Only check distance if lat/lon exist
        if record.latitude and record.longitude and record.isTracked:
            old_coords = (float(record.latitude), float(record.longitude))
            new_coords = (float(lat), float(lon))

            if geodesic(old_coords, new_coords).km < 15:
                record.save()
                return Response({'message': 'Location has not changed'}, status=status.HTTP_202_ACCEPTED)

        # Update location info
        record.latitude = lat
        record.longitude = lon
        record.location = location
        record.save()

        return Response({"status": "Location updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in get_update_location: {str(e)}")
        return Response({"error": f"Error in get_update_location: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def otp_send(request):
    try:
        phone = request.data.get('phoneNumber')

        if not phone:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        verification = twilio_number_verification(phone)

        return Response({"status": verification }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in opt_send: {str(e)}")
        return Response({"error": f"Error in opt_send: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_otp(request):
    try:
        phone = request.data.get('phoneNumber')
        code = request.data.get('code')

        if not phone or not code:
            return Response({'error': 'Phone number and code are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        verification_check = twilio_number_verification_status(phone, code)

        if verification_check:
            return Response({"status":"approved","message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        
        return Response({"status":"failed", "message":"Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error in verify_otp: {str(e)}")
        return Response({"error": f"Error in verify_otp: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_tracking(request):
    try:
        user = request.user

        user_location = UserLocationDetail.objects.get(user=user)

        if user_location:
            user_location.isTracked = False
            user_location.save()


        return Response({"message": "Tracking Stopped"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.error(f"Error in Stop Tracking: {str(e)}")
        return Response({"error": f"Error in stop_tracking: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)