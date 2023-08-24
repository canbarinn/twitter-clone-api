#REMINDER: HTTP request passed into the url and it goes to the
#view class, which is CreateUserView, it is based on generics.CreateAPIView:
#it handles post requests designed for creating objects in data base It handles
#all of the logic for you. All you need to do is set serializer like UserSerialier
#in serializers.py and set is serializer_class as UserSerializer to know which serializer
#or model we use. Serializer then create the object and return the necessary response.

"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions, viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer, FollowSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema



class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

class FollowViewSet(viewsets.ModelViewSet):
    """Manage following users."""
    serializer_class = FollowSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        follows = request.user.follows.all().order_by('-id')
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=FollowSerializer
    )
    def follow(self, request):
        follow_id = request.data.get('id')
        user_to_be_followed = get_user_model().objects.get(id=follow_id)
        request.user.follows.add(user_to_be_followed)
        return Response({"message": "Followed."}, status=status.HTTP_200_OK)


