from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Category
from category import serializers
from category.renderers import CategoryJsonRenderer


class CategoryViewset(viewsets.ModelViewSet):
    """Manage categories"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CategoryJsonRenderer,)
