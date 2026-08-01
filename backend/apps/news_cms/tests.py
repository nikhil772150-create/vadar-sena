from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.common.enums import UserType
from apps.news_cms.models import NewsCategory, News, StaticPage, FAQ, NewsStatus
from apps.news_cms.services import NewsCMSService

User = get_user_model()


class NewsCMSTest(TestCase):
    def setUp(self):
        self.category = NewsCategory.objects.create(name="Press Releases", slug="press-releases")
        self.news = News.objects.create(
            title="Sena Annual Convention Announced",
            slug="sena-annual-convention-announced",
            category=self.category,
            content="Details of the convention...",
            status=NewsStatus.PUBLISHED
        )
        self.admin = User.objects.create_user(
            phone_number="9876543210",
            password="adminpassword123",
            user_type=UserType.ADMIN,
            is_staff=True
        )
        self.client = APIClient()

    def test_public_news_list(self):
        response = self.client.get('/api/v1/news-cms/news/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_news_publication_service(self):
        draft_news = News.objects.create(
            title="Draft News",
            slug="draft-news",
            content="Draft content",
            status=NewsStatus.DRAFT
        )
        NewsCMSService.publish_news(draft_news)
        self.assertEqual(draft_news.status, NewsStatus.PUBLISHED)
        self.assertIsNotNone(draft_news.published_at)

    def test_static_pages_api(self):
        StaticPage.objects.create(
            title="About Us",
            slug="about-us",
            content="About Bharatiya Vadar Sena"
        )
        response = self.client.get('/api/v1/news-cms/pages/about-us/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "About Us")
