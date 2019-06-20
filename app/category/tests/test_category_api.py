from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Category
from category.serializers import CategorySerializer


CATEGORY_URL = reverse('category:category-list')


def category_details_url(id):
    """Return category details url"""
    return reverse('category:category-detail', args=[id])


def sample_category(name='place'):
    """Create and return a sample category"""
    return Category.objects.create(name=name)


class PublicFavoritesApiTests(TestCase):
    """Test the publically available favorite things API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryApiTests(TestCase):
    """test authenticated favorite api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_categories(self):
        """Test retreiving a list of categories"""
        sample_category()
        sample_category(name="people")
        res = self.client.get(CATEGORY_URL)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 2)
        self.assertEqual(len(res.data['results']), len(serializer.data))
        self.assertEqual(res.data['results'], serializer.data)

    def test_get_category_details(self):
        """"test viewing category details"""
        category = sample_category()
        url = category_details_url(category.id)
        res = self.client.get(url)
        serializer = CategorySerializer(category)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category(self):
        """Test creating a category"""
        payload = {
            'name': 'Houses',
        }
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(id=res.data['id'])
        serializer = CategorySerializer(category)
        self.assertEqual(serializer.data['name'], payload['name'])

    def test_create_category_with_invalid_details_fails(self):
        """Test creating a category with invalid details"""
        res = self.client.post(CATEGORY_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['errors']['name'][0],
            'This field is required.')

    def test_create_category_with_existing_name(self):
        """Test create category with existing same name fails"""
        sample_category()
        res = self.client.post(CATEGORY_URL, {"name": "place"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['errors']['name'][0],
            'This field must be unique.')

    def test_update_category(self):
        """Test updating a favorite thing with  put"""
        category = sample_category()
        url = category_details_url(category.id)
        self.client.put(url, {"name": "school"})
        category.refresh_from_db()
        self.assertEqual(category.name, 'school')

    def test_update_category_to_existing_name(self):
        """Test updating a category to existing name fails"""
        sample_category()
        category = sample_category(name='House')
        url = category_details_url(category.id)
        res = self.client.put(url, {"name": "place"})

        category.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['errors']['name'][0],
            'This field must be unique.')
