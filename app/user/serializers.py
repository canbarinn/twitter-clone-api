"""
Serializers for the user API View.
"""

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from core.models import Tweet

from rest_framework import serializers



class FollowSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
        )
        read_only_fields = ['username', 'email']

class LikedTweetSerializer(serializers.ModelSerializer):

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

    followers = FollowSerializer(many=True)
    follows = FollowSerializer(many=True)
    likes = LikedTweetSerializer(many=True)

    class Meta:
        model = get_user_model()
    # REMINDER: We are not including is_staff or is_active because
    # we do not want user to set those themselves. This should done by admins.
        fields = ['id', 'email', 'password', 'username', 'follows', 'followers', 'likes']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


    def create(self, validated_data):
        user_follows = validated_data.pop('follows', [])
        user_followers = validated_data.pop('followers', [])
        likes = validated_data.pop('likes', [])
        user = get_user_model().objects.create(**validated_data)

        if user_follows is not None:
            for follow in user_follows:
                for attr, value in follow:
                    setattr(user.follows, attr, value)

        if user_followers is not None:
            for follower in user_followers:
                for attr, value in follower:
                    setattr(user.followers, attr, value)

        if likes is not None:
            for like in likes:
                for attr, value in like:
                    setattr(user.likes, attr, value)

        return user

    def update(self, instance, validated_data):
        user_follows = validated_data.pop('follows', [])
        user_followers = validated_data.pop('followers', [])
        likes = validated_data.pop('likes', [])

        if user_follows is not None:
            for follow in user_follows:
                for attr,value in follow:
                    setattr(instance.follows, attr, value)

        if user_followers is not None:
            for follower in user_followers:
                for attr,value in follower:
                    setattr(instance.followers, attr, value)

        if likes is not None:
            for user_liked in likes:
                for attr, value in user_liked:
                    setattr(instance.likes, attr, value)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            name=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with ')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


