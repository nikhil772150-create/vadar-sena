from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Operation successful", http_status=status.HTTP_200_OK):
    """
    Standardized success API response envelope.
    """
    return Response({
        "success": True,
        "message": message,
        "data": data if data is not None else {},
        "errors": None
    }, status=http_status)


def error_response(errors=None, message="Operation failed", http_status=status.HTTP_400_BAD_REQUEST):
    """
    Standardized error API response envelope.
    """
    return Response({
        "success": False,
        "message": message,
        "data": None,
        "errors": errors if errors is not None else []
    }, status=http_status)
