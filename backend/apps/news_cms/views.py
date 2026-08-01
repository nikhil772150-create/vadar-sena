from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.responses import success_response, error_response
from apps.common.permissions import IsAdminUserOrSuperAdmin
from apps.news_cms.models import NewsCategory, News, StaticPage, FAQ, HomepageBanner, NewsStatus
from apps.news_cms.serializers import (
    NewsCategorySerializer,
    NewsSerializer,
    StaticPageSerializer,
    FAQSerializer,
    HomepageBannerSerializer
)
from apps.news_cms.services import NewsCMSService


class NewsCategoryViewSet(viewsets.ModelViewSet):
    queryset = NewsCategory.objects.filter(is_deleted=False)
    serializer_class = NewsCategorySerializer
    search_fields = ['name', 'slug']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]

    def perform_create(self, serializer):
        slug = NewsCMSService.generate_unique_slug(NewsCategory, serializer.validated_data['name'])
        serializer.save(slug=slug)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_deleted=False).select_related('category', 'cover_asset')
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'is_pinned', 'is_featured']
    search_fields = ['title', 'content', 'slug']
    ordering_fields = ['is_pinned', 'published_at', 'created_at', 'title']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'public_feed']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]

    def get_queryset(self):
        qs = super().get_queryset()
        # Public users see published news only
        if not (self.request.user and self.request.user.is_authenticated and self.request.user.user_type in ['ADMIN', 'SUPERADMIN']):
            qs = qs.filter(status=NewsStatus.PUBLISHED)
        return qs

    def perform_create(self, serializer):
        slug = NewsCMSService.generate_unique_slug(News, serializer.validated_data['title'])
        serializer.save(slug=slug)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def publish(self, request, pk=None):
        news = self.get_object()
        NewsCMSService.publish_news(news)
        return success_response(NewsSerializer(news).data, "News published successfully.")

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUserOrSuperAdmin])
    def archive(self, request, pk=None):
        news = self.get_object()
        NewsCMSService.archive_news(news)
        return success_response(NewsSerializer(news).data, "News archived successfully.")


class StaticPageViewSet(viewsets.ModelViewSet):
    queryset = StaticPage.objects.filter(is_deleted=False)
    serializer_class = StaticPageSerializer
    lookup_field = 'slug'
    search_fields = ['title', 'content', 'slug']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]

    def perform_create(self, serializer):
        slug = NewsCMSService.generate_unique_slug(StaticPage, serializer.validated_data['title'])
        serializer.save(slug=slug)


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.filter(is_deleted=False, is_active=True)
    serializer_class = FAQSerializer
    search_fields = ['question', 'answer']
    ordering_fields = ['display_order', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]


class HomepageBannerViewSet(viewsets.ModelViewSet):
    queryset = HomepageBanner.objects.filter(is_deleted=False, is_active=True)
    serializer_class = HomepageBannerSerializer
    ordering_fields = ['display_order', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminUserOrSuperAdmin()]
