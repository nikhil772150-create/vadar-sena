from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.communications.views import ContactInquiryViewSet, NotificationViewSet

router = DefaultRouter()
router.register('contact', ContactInquiryViewSet, basename='contact-inquiry')
router.register('notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
