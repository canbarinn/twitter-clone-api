"""
Serializers for the user API View.
"""

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from core.models import Tweet, User

from rest_framework import serializers


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for follows list."""
    id = serializers.IntegerField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'name',
            'email',
        )
        read_only_fields = ['name', 'email']


class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for profile pictures."""

    class Meta:
        model = User
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


class LikedTweetSerializer(serializers.ModelSerializer):
    """Serializer for likes."""
    id = serializers.IntegerField()

    class Meta:
        model = Tweet
        fields = (
            'id',
            'tweet_text',
        )
        read_only_fields = ['tweet_text']


class UserSerializer( serializers.ModelSerializer):
    """Serializer for the user object."""
    followers = FollowSerializer(many=True, required=False)
    follows = FollowSerializer(many=True, required=False)
    likes = LikedTweetSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'name', 'follows', 'followers', 'likes', 'image']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create an user."""
        user_follows = validated_data.pop('follows', [])
        user_followers = validated_data.pop('followers', [])
        likes = validated_data.pop('likes', [])
        image = validated_data.pop('image', [])
        user = get_user_model().objects.create(**validated_data)

        for list, list_field in [
            (user_follows, user.follows),
            (user_followers, user.followers),
            (likes, user.likes),
            (image, user.image)
            ]:
            if list is not None:
                for item in list:
                    for attr, value in item:
                        setattr(list_field, attr, value)

        return user


    def update(self, instance, validated_data):
        """Update an user."""
        user_follows = validated_data.pop('follows', [])
        user_followers = validated_data.pop('followers', [])
        likes = validated_data.pop('likes', [])
        image = validated_data.pop('image', [])

        for list, list_field in [
            (user_follows, instance.follows),
            (user_followers, instance.followers),
            (likes, instance.likes),
            (image, instance.image)
            ]:

            if list is not None:
                for item in list:
                    for attr, value in item:
                        setattr(list_field, attr, value)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

