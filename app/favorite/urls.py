from django.urls import path, include
from rest_framework.routers import DefaultRouter
from favorite import views

app_name = 'favorite'
router = DefaultRouter()
router.register('favorites', views.FavoriteViewset)

urlpatterns = [
    path('', include(router.urls))
]
