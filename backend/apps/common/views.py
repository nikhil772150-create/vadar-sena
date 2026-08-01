from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import connection
from django.conf import settings
import os

from apps.common.responses import success_response


class HealthCheckView(APIView):
    """
    GET /api/v1/health/
    System operational status check.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Check database connection
        db_healthy = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
        except Exception:
            db_healthy = False

        status_data = {
            "status": "Healthy" if db_healthy else "Degraded",
            "version": "1.0.0",
            "environment": os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.local'),
            "database": {
                "connected": db_healthy,
                "engine": settings.DATABASES['default']['ENGINE']
            },
            "debug": settings.DEBUG
        }

        return success_response(status_data, "System health check")
