"""
Views for the tweet APIs.
"""
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


class LikeView(APIView):
    """View for manage likes."""
    serializer_class = serializers.LikeSerializer
    queryset = Tweet.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, tweet_id):
        """Like tweet."""
        tweet = Tweet.objects.get(id=tweet_id)
        tweet.likes.add(request.user)
        return Response({'message':'Tweet liked.'}, status=status.HTTP_200_OK)

    def delete(self, request, tweet_id):
        """Remove like from previously liked tweet."""
        tweet = Tweet.objects.get(id=tweet_id)
        tweet.likes.remove(request.user)
        return Response({'message':'Like is removed.'}, status=status.HTTP_200_OK)