from rest_framework.views import exception_handler
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Add custom error handling
    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': 'An error occurred',
                'details': response.data
            }
        }
        
        # Log the error
        logger.error(f"API Error: {response.status_code} - {response.data}")
        
        response.data = custom_response_data
    
    return response

