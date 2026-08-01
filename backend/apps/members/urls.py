from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.members.views import MemberViewSet, VerifyCardView

router = DefaultRouter()
router.register('', MemberViewSet, basename='member')

urlpatterns = [
    path('verify-card/<str:qr_token>/', VerifyCardView.as_view(), name='member-verify-card'),
    path('', include(router.urls)),
]
