from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.donations.views import DonationViewSet

router = DefaultRouter()
router.register('', DonationViewSet, basename='donation')

urlpatterns = [
    path('', include(router.urls)),
]
