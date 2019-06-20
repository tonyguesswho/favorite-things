from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Favorite, Category
from favorite.serializers import FavoriteDetailsSerializer, FavoriteSerializer


FAVORITE_URL = reverse('favorite:favorite-list')


def favorite_details_url(id):
    """Return favorite thing details url"""
    return reverse('favorite:favorite-detail', args=[id])


def sample_favorite_thing(user, **params):
    """create and return a sample favorite thing"""
    defaults = {
        'title': 'lagos',
        'description': "",
        'ranking': 1
    }
    defaults.update(params)
    return Favorite.objects.create(user=user, **defaults)


def sample_category(name='place'):
    """Create and return a sample category"""
    return Category.objects.create(name=name)


class PublicFavoritesApiTests(TestCase):
    """Test the publically available favorite things API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access this endpoint"""
        res = self.client.get(FAVORITE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """test authenticated favorite api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_favorite_things(self):
        """Test retreiving a list of recipe"""
        sample_favorite_thing(
            user=self.user,
            title="peter",
            category=sample_category(name='people'))
        sample_favorite_thing(
            user=self.user,
            category=sample_category())

        res = self.client.get(FAVORITE_URL)

        favorite_things = Favorite.objects.all()
        serializer = FavoriteDetailsSerializer(favorite_things, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(serializer.data))
        self.assertEqual(res.data, serializer.data)

    def test_favorite_list_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'password'
        )
        sample_favorite_thing(
            user=self.user,
            title="peter",
            category=sample_category(name='people'))
        sample_favorite_thing(
            user=user2,
            category=sample_category())

        res = self.client.get(FAVORITE_URL)
        favorite_things = Favorite.objects.filter(user=self.user)
        serializer = FavoriteDetailsSerializer(favorite_things, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_get_favorite_thing_details(self):
        """"test viewing favorite things details"""
        favorite_thing = sample_favorite_thing(
            user=self.user,
            category=sample_category())
        url = favorite_details_url(favorite_thing.id)
        res = self.client.get(url)
        serializer = FavoriteDetailsSerializer(favorite_thing)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_favorite_thing(self):
        """Test creating a favorite thing"""
        category = sample_category()
        payload = {
            'title': 'tfish',
            'description': "",
            'ranking': 1,
            'categoryId': category.id
        }
        res = self.client.post(FAVORITE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        favorite_thing = Favorite.objects.get(id=res.data['id'])
        serializer = FavoriteSerializer(favorite_thing)
        self.assertEqual(serializer.data['title'], payload['title'])

    def test_create_favorite_thing_with_invalid_details_fails(self):
        """Test creating a favorite thing with invalid details"""
        payload = {
            'title': 'tfish',
            'description': "invalid",
            'ranking': 'b',
            'categoryId': 90
        }
        res = self.client.post(FAVORITE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['description'][0],
            'description is not up to ten characters')
        self.assertEqual(
            res.data['ranking'][0],
            'A valid integer is required.')
        self.assertEqual(
            res.data['categoryId'][0],
            'The category id does not exist.')

    def test_create_favorite_thing_with_same_title(self):
        """Test create favorite thing with same title fails for same user"""
        category = sample_category()
        payload = {
            'title': 'lagos',
            'description': "",
            'ranking': 10,
            'categoryId': category.id
        }
        sample_favorite_thing(
            user=self.user,
            category=category)
        res = self.client.post(FAVORITE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['title'][0],
            'Title already exists')

    def test_create_favorite_thing_with_same_title_different_users(self):
        """Test create favorite thing with same title fails for same user"""

        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'password'
        )
        category = sample_category()
        payload = {
            'title': 'lagos',
            'description': "",
            'ranking': 1,
            'categoryId': category.id
        }
        sample_favorite_thing(
            user=self.user,
            category=category)
        user_client = APIClient()
        user_client.force_authenticate(user2)
        res = user_client.post(FAVORITE_URL, payload)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_partial_update_favorite_thing(self):
        """Test updating a favorite thing with patch"""
        category = sample_category()
        favorite_thing = sample_favorite_thing(
            user=self.user,
            category=category)
        url = favorite_details_url(favorite_thing.id)
        self.client.patch(url, {'title': 'hand'})

        favorite_thing.refresh_from_db()
        self.assertEqual(favorite_thing.title, 'hand')

    def test_full_update_favorite_thing(self):
        """Test updating a favorite thing with  put"""
        category = sample_category()
        favorite_thing = sample_favorite_thing(
            user=self.user,
            category=category)
        url = favorite_details_url(favorite_thing.id)
        payload = {
            'title': 'table',
            'description': "",
            'ranking': 10,
            'categoryId': category.id
        }
        self.client.put(url, payload)

        favorite_thing.refresh_from_db()
        self.assertEqual(favorite_thing.title, payload['title'])
        self.assertEqual(favorite_thing.description, payload['description'])
        self.assertEqual(favorite_thing.ranking, payload['ranking'])

    def test_update_favorite_thing_with_same_title(self):
        """Test updating a favorite thing with  put"""
        category = sample_category()
        favorite_thing = sample_favorite_thing(
            user=self.user,
            category=category)
        url = favorite_details_url(favorite_thing.id)
        payload = {
            'title': 'lagos',
            'description': "",
            'ranking': 10,
            'categoryId': category.id
        }
        self.client.put(url, payload)

        favorite_thing.refresh_from_db()
        self.assertEqual(favorite_thing.title, payload['title'])
        self.assertEqual(favorite_thing.description, payload['description'])
        self.assertEqual(favorite_thing.ranking, payload['ranking'])

    def test_updating_rankings_adjust_other_ranks(self):
        """Test updating a favorite things rank adjusts other ranks"""
        category = sample_category()
        favorite_thing = sample_favorite_thing(
            user=self.user,
            category=category)
        favorite_thing_2 = sample_favorite_thing(
            user=self.user,
            category=category,
            ranking=2,
            title='Benin')
        url = favorite_details_url(favorite_thing_2.id)
        payload = {
            'title': 'Benin',
            'description': "",
            'ranking': 1,
            'categoryId': category.id
        }
        self.client.put(url, payload)

        favorite_thing_2.refresh_from_db()
        favorite_thing.refresh_from_db()
        self.assertEqual(favorite_thing_2.ranking, 1)
        self.assertEqual(favorite_thing.ranking, 2)

    def test_update_with_same_rank(self):
        """Test update favorites with same rank dose not adjust other ranks"""
        category = sample_category()
        favorite_thing = sample_favorite_thing(
            user=self.user,
            category=category)
        favorite_thing_2 = sample_favorite_thing(
            user=self.user,
            category=category,
            ranking=2,
            title='Benin')
        url = favorite_details_url(favorite_thing.id)
        payload = {
            'title': 'lagos',
            'description': "",
            'ranking': 1,
            'categoryId': category.id
        }
        self.client.put(url, payload)

        favorite_thing_2.refresh_from_db()
        self.assertEqual(favorite_thing_2.ranking, 2)
