# middleware.py
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"An exception occurred: {exception}")
        return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
