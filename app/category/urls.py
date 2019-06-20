from django.urls import path, include
from rest_framework.routers import DefaultRouter
from category import views

app_name = 'category'
router = DefaultRouter()
router.register('categories', views.CategoryViewset)

urlpatterns = [
    path('', include(router.urls))
]
