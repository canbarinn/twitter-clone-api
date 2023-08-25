"""
Serializers for tweet APIs
"""
from rest_framework import serializers
from core.models import Tweet, User
from django.contrib.auth import get_user_model


class LikedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )
        read_only_fields = ['username', 'email']



class TweetSerializer(serializers.ModelSerializer):
    """Serializer for tweets."""

    likes = LikedUserSerializer(many=True)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'tweet_text', 'likes', 'created', 'updated']
        read_only_fields = ['id']

    def create(self, validated_data):
        likes = validated_data.pop('likes', [])
        tweet = Tweet.objects.create(**validated_data)

        if likes is not None:
            for like in likes:
                for attr, value in like:
                    setattr(tweet.likes, attr, value)

        return tweet

    def update(self, instance, validated_data):
        likes = validated_data.pop('likes', [])

        if likes is not None:
            for tweet_liked in likes:
                for attr,value in tweet_liked:
                    setattr(instance,attr,value)

        for attr,value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class TweetDetailSerializer(TweetSerializer):
    """Serializer for tweet detail view."""

    class Meta(TweetSerializer.Meta):
        fields = TweetSerializer.Meta.fields



