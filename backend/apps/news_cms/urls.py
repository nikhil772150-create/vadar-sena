from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.news_cms.views import (
    NewsCategoryViewSet,
    NewsViewSet,
    StaticPageViewSet,
    FAQViewSet,
    HomepageBannerViewSet
)

router = DefaultRouter()
router.register('categories', NewsCategoryViewSet, basename='news-category')
router.register('news', NewsViewSet, basename='news')
router.register('pages', StaticPageViewSet, basename='static-page')
router.register('faqs', FAQViewSet, basename='faq')
router.register('banners', HomepageBannerViewSet, basename='banner')

urlpatterns = [
    path('', include(router.urls)),
]
