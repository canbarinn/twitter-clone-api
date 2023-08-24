"""
Views for the tweet APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tweet
from tweet import serializers


class TweetViewSet(viewsets.ModelViewSet):
    """View for manage tweet APIs."""
    serializer_class = serializers.TweetDetailSerializer
    queryset = Tweet.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tweets for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for requests."""
        if self.action == 'list':
            return serializers.TweetSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new tweet."""
        serializer.save(user=self.request.user)
