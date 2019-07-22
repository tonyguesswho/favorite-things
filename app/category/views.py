from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from core.models import Category
from category import serializers


class CategoryViewset(viewsets.ModelViewSet):
    """Manage categories"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = None
