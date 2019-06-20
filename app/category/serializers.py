from rest_framework import serializers
from core.models import Category
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category object"""
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)
