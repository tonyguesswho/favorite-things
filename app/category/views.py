from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Category
from favorite import serializers


class CategoryViewset(viewsets.ModelViewSet):
    """Manage categories"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
