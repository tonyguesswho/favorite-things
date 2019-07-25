from django.urls import path, include
from rest_framework.routers import DefaultRouter
from favorite import views

app_name = 'favorite'
router = DefaultRouter()
router.register('favorites', views.FavoriteViewset)
router.register('history', views.FavoriteHistoryViewset, base_name="history")

urlpatterns = [
    path('', include(router.urls))
]
