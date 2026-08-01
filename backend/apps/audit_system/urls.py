from django.urls import path
from django.http import JsonResponse

def audit_health_check(request):
    return JsonResponse({"module": "audit_system", "status": "active"})

urlpatterns = [
    path('health/', audit_health_check, name='audit-health'),
]
