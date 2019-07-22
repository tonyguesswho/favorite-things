from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Favorite, CoreHistoricalfavorite
from favorite import serializers
from favorite.renderers import FavoriteJsonRenderer
from rest_framework.response import Response
from core.helpers.favorite_things import adjust_ranking


class FavoriteViewset(viewsets.ModelViewSet):
    """Manage favorite things"""
    queryset = Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer
    authentication_classes = (TokenAuthentication,)
    renderer_classes = (FavoriteJsonRenderer,)
    permission_classes = (IsAuthenticated,)
    filter_fields = ('category_id',)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('ranking')

    def get_serializer_class(self):
        """Return serializer class"""
        if self.action == 'retrieve' or self.action == 'list':
            return serializers.FavoriteDetailsSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """create a new favorite thing"""
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        adjust_ranking(request, None, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteHistoryViewset(viewsets.ReadOnlyModelViewSet):
    """Manage audits for favorite things"""
    queryset = CoreHistoricalfavorite.objects.all()
    serializer_class = serializers.HistorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(
            history_user=self.request.user).order_by('-history_date')

    def get_serializer_class(self):
        """Return serializer class"""
        return self.serializer_class
