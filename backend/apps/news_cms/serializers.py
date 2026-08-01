from rest_framework import serializers
from apps.news_cms.models import NewsCategory, News, StaticPage, FAQ, HomepageBanner


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'uuid', 'name', 'slug', 'description', 'created_at')
        read_only_fields = ('id', 'uuid', 'created_at')


class NewsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id', 'uuid', 'title', 'slug', 'category', 'category_name',
            'content', 'cover_asset', 'cover_url', 'status', 'is_pinned',
            'is_featured', 'published_at', 'meta_title', 'meta_description',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'uuid', 'slug', 'created_at', 'updated_at')

    def get_cover_url(self, obj):
        if obj.cover_asset and obj.cover_asset.file:
            return obj.cover_asset.file.url
        return None


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ('id', 'uuid', 'slug', 'title', 'content', 'meta_title', 'meta_description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'uuid', 'created_at', 'updated_at')


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id', 'uuid', 'question', 'answer', 'display_order', 'is_active', 'created_at')
        read_only_fields = ('id', 'uuid', 'created_at')


class HomepageBannerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HomepageBanner
        fields = ('id', 'uuid', 'title', 'image_asset', 'image_url', 'link_url', 'display_order', 'is_active', 'created_at')
        read_only_fields = ('id', 'uuid', 'created_at')

    def get_image_url(self, obj):
        if obj.image_asset and obj.image_asset.file:
            return obj.image_asset.file.url
        return None
