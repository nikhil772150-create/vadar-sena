from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.events_meetings.views import EventViewSet, MeetingViewSet

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('meetings', MeetingViewSet, basename='meeting')

urlpatterns = [
    path('', include(router.urls)),
]
