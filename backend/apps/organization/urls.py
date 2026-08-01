from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.organization.views import (
    StateViewSet,
    DistrictViewSet,
    TalukaViewSet,
    VillageViewSet,
    DesignationViewSet
)

router = DefaultRouter()
router.register('states', StateViewSet, basename='state')
router.register('districts', DistrictViewSet, basename='district')
router.register('talukas', TalukaViewSet, basename='taluka')
router.register('villages', VillageViewSet, basename='village')
router.register('designations', DesignationViewSet, basename='designation')

urlpatterns = [
    path('', include(router.urls)),
]
