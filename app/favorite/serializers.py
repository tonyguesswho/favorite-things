from rest_framework import serializers
from core.models import Favorite, Category, CoreHistoricalfavorite
from category.serializers import CategorySerializer
from django.utils.translation import ugettext_lazy as _
from core.helpers.favorite_things import adjust_ranking


class FavoriteSerializer(serializers.ModelSerializer):
    """Serilize favorite things"""

    categoryId = serializers.PrimaryKeyRelatedField(
        error_messages={
            'does_not_exist': _('The category id does not exist.'),
            'required': _('Category Id is required.'),
            'incorrect_type': _('The category Id should be a string.'),
        },
        queryset=Category.objects.all(), source='category'
    )

    createdDate = serializers.SerializerMethodField(
        method_name='get_created_at')

    modifiedDate = serializers.SerializerMethodField(
        method_name='get_updated_at')

    metadata = serializers.JSONField(required=False)

    class Meta:
        model = Favorite
        fields = ('id',
                  'title',
                  'description',
                  'metadata',
                  'ranking',
                  'categoryId', 'createdDate', 'modifiedDate',)
        read_only_fields = ('id',)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    def validate_title(self, value):
        request = self.context.get('request')
        """
        Check that the title is unique to the user.
        """
        try:
            favorite_thing = Favorite.objects.get(
                title=value.lower(),
                user=request.user.id)
        except Favorite.DoesNotExist:
            return value.lower()
        if self.instance and favorite_thing.id == self.instance.id:
            return value.lower()
        else:
            raise serializers.ValidationError(_("Title already exists"))

    def create(self, validated_data):
        request = self.context.get('request')
        total_fav = Favorite.objects.filter(
            user=request.user,
            category=validated_data['category']).count()
        ranking = validated_data['ranking']
        if ranking > total_fav:
            validated_data['ranking'] = total_fav + 1
        adjust_ranking(request, validated_data)
        return super(FavoriteSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        total_fav = Favorite.objects.filter(
            user=request.user,
            category=validated_data['category']).count()
        ranking = validated_data['ranking']
        if ranking >= total_fav:
            validated_data['ranking'] = total_fav
        adjust_ranking(request, validated_data, instance)
        return super(FavoriteSerializer, self).update(instance, validated_data)


class FavoriteDetailsSerializer(serializers.ModelSerializer):
    """Serilize favorite things"""

    category = CategorySerializer(read_only=True)

    createdDate = serializers.SerializerMethodField(
        method_name='get_created_at')
    modifiedDate = serializers.SerializerMethodField(
        method_name='get_updated_at')

    class Meta:
        model = Favorite
        fields = ('id',
                  'title',
                  'description',
                  'ranking',
                  'category',
                  'metadata',
                  'createdDate',
                  'modifiedDate',)
        read_only_fields = ('id',)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class HistorySerializer(serializers.ModelSerializer):
    """Serializer for favorite audit object"""

    class Meta:
        model = CoreHistoricalfavorite
        fields = '__all__'
