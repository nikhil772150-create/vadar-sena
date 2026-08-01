from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def api_root_view(request):
    return JsonResponse({
        "system": "Bharatiya Vadar Sena Management System (BVSMS) API",
        "version": "1.0.0",
        "status": "Operational"
    })


urlpatterns = [
    path('', api_root_view, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.common.urls')),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/organization/', include('apps.organization.urls')),
    path('api/v1/members/', include('apps.members.urls')),
    path('api/v1/events-meetings/', include('apps.events_meetings.urls')),
    path('api/v1/news-cms/', include('apps.news_cms.urls')),
    path('api/v1/gallery/', include('apps.gallery.urls')),
    path('api/v1/donations/', include('apps.donations.urls')),
    path('api/v1/communications/', include('apps.communications.urls')),
    path('api/v1/analytics/', include('apps.reports_analytics.urls')),
    path('api/v1/audit/', include('apps.audit_system.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
