"""
Serializers for tweet APIs
"""
from rest_framework import serializers
from core.models import Tweet, User
from django.contrib.auth import get_user_model


class LikedUserSerializer(serializers.ModelSerializer):
    """Serializer for likes."""

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'name',
            'email',
        )
        read_only_fields = ['name', 'email']


class TweetSerializer(serializers.ModelSerializer):
    """Serializer for tweets."""
    likes = LikedUserSerializer(many=True, required=False)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'tweet_text', 'likes', 'created', 'updated']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create tweet."""
        tweet = Tweet.objects.create(**validated_data)
        return tweet

    def update(self, instance, validated_data):
        """Update tweet."""
        for attr,value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TweetDetailSerializer(TweetSerializer):
    """Serializer for tweet detail view."""

    class Meta(TweetSerializer.Meta):
        fields = TweetSerializer.Meta.fields


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for like tweet view."""
    id = serializers.IntegerField()

    class Meta():
        model = Tweet
        fields = ['id']