import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Global exception handler wrapping all DRF exception responses
    into the unified JSON envelope ({ success: false, message, errors }).
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            "success": False,
            "message": "An error occurred while processing your request.",
            "data": None,
            "errors": response.data
        }

        if isinstance(response.data, dict):
            if "detail" in response.data:
                custom_data["message"] = str(response.data["detail"])
            elif "non_field_errors" in response.data:
                custom_data["message"] = str(response.data["non_field_errors"][0])

        response.data = custom_data
    else:
        logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
        response = Response({
            "success": False,
            "message": "Internal Server Error. Please contact administrator.",
            "data": None,
            "errors": [str(exc)]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
