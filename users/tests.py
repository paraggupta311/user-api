import logging
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

logger = logging.getLogger(__name__)

class UserAPITests(APITestCase):

    def setUp(self):
        User.objects.create(first_name="James", last_name="Smith", company_name="ABC Corp", age=35, city="NYC", state="NY", zip=10001, email="james@example.com", web="http://abc.com")
        User.objects.create(first_name="Emily", last_name="Jameson", company_name="XYZ Inc", age=28, city="LA", state="CA", zip=90001, email="emily@example.com", web="http://xyz.com")
        User.objects.create(first_name="Mike", last_name="Johnson", company_name="Delta", age=42, city="Houston", state="TX", zip=77001, email="mike@example.com", web="http://delta.com")
        logger.info("Test users created in setUp")

    def test_get_all_users_default_limit(self):
        logger.info("Testing GET all users with default limit")
        response = self.client.get('/api/users/')
        logger.info(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_pagination_limit(self):
        logger.info("Testing pagination limit=2")
        response = self.client.get('/api/users/?limit=2')
        logger.info(f"Response data: {response.data}")
        self.assertEqual(len(response.data), 2)

    def test_name_filter_case_insensitive(self):
        logger.info("Testing name filter with 'jam'")
        response = self.client.get('/api/users/?name=jam')
        names = [user['first_name'] + user['last_name'] for user in response.data]
        logger.info(f"Filtered names: {names}")
        self.assertTrue(any('James' in name or 'Jameson' in name for name in names))

    def test_sort_descending_age(self):
        logger.info("Testing sort by descending age")
        response = self.client.get('/api/users/?sort=-age')
        ages = [user['age'] for user in response.data]
        logger.info(f"Ages: {ages}")
        self.assertEqual(ages, sorted(ages, reverse=True))

    def test_combined_filters(self):
        logger.info("Testing combined filters: page=1, limit=1, name=james, sort=-age")
        response = self.client.get('/api/users/?page=1&limit=1&name=james&sort=-age')
        logger.info(f"Response: {response.data}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertIn('James', response.data[0]['first_name'] or response.data[0]['last_name'])
