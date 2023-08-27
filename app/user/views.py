"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions, viewsets, status
from rest_framework.settings import api_settings
from user.serializers import UserSerializer,  FollowSerializer, UserImageSerializer#, AuthTokenSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
    

class AuthToken(ObtainAuthToken):
    """Create a new auth token for user."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class FollowViewSet(viewsets.ModelViewSet):
    """Manage following users."""
    serializer_class = FollowSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """List follows."""
        follows = request.user.follows.all().order_by('-id')
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def follow(self, request):
        """Follow user."""
        follow_id = request.data.get('id')
        user_to_be_followed = get_user_model().objects.get(id=follow_id)
        request.user.follows.add(user_to_be_followed)
        return Response({"message": "Followed."}, status=status.HTTP_200_OK)

    def unfollow(self, request):
        """Unfollow user."""
        unfollow_id = request.data.get('id')
        user_to_be_unfollowed = get_user_model().objects.get(id=unfollow_id)
        request.user.follows.remove(user_to_be_unfollowed)
        return Response({"message": "Unfollowed."},status=status.HTTP_200_OK)


class UploadProfilePictureView(APIView):
    """Manage profile picture."""
    serializer_class = UserImageSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        """Upload a profile image."""
        user = self.request.user
        serializer = UserImageSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

