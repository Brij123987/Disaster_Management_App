from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail

import logging
import logging.config
from django.conf import settings

# Apply Django's logging config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('custom_logger')



@api_view(['POST'])
def send_user_support_email(request):
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        subject = request.data.get('subject')
        message = request.data.get('message')
        inquiryType = request.data.get('inquiryType')

        recipient_list = ['brijeshyadav9811@gmail.com']

        full_message = f"Message from {name} & {email} and Inquiry Type: {inquiryType} \n\n {message}"

        send_mail(subject, full_message, email, recipient_list, fail_silently=False)


        return Response({"msg":"Message sent successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in send_user_support_email: {str(e)}")
        return Response({"error":f"Error in send_user_support_email: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)