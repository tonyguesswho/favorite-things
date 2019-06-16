from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerilaizer, AuthTokenSerilaizer


class CreateUserView(generics.CreateAPIView):
    """Creates a new user"""
    serializer_class = UserSerilaizer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerilaizer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserview(generics.RetrieveUpdateAPIView):
    """Api to get and update user details"""
    serializer_class = UserSerilaizer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retreive and retun auth user"""
        return self.request.user
