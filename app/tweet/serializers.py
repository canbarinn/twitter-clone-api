"""
Serializers for tweet APIs
"""
from rest_framework import serializers
from core.models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    """Serializer for tweets."""

    class Meta:
        model = Tweet
        fields = ['id', 'tweet_text', 'created', 'updated']
        read_only_fields = ['id']


class TweetDetailSerializer(TweetSerializer):
    """Serializer for tweet detail view."""

    class Meta(TweetSerializer.Meta):
        fields = TweetSerializer.Meta.fields
