from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Favorite
from favorite import serializers


class FavoriteViewset(viewsets.ModelViewSet):
    """Manage favorite things"""
    queryset = Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return serializer class"""
        if self.action == 'retrieve' or self.action == 'list':
            return serializers.FavoriteDetailsSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """create a new favorite thing"""
        serializer.save(user=self.request.user)
