"""Tests for tweet APIs."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tweet
from tweet.serializers import TweetSerializer, TweetDetailSerializer

TWEETS_URL = reverse('tweet:tweet-list')

def detail_url(tweet_id):
    """Create and return a tweet detail URL."""
    return reverse('tweet:tweet-detail', args=[tweet_id])

def create_tweet(user, **params):
    """Create and return a sample tweet."""
    defaults = {
        'tweet_text': 'This is my first tweet.'
    }
    defaults.update(params)

    tweet = Tweet.objects.create(user=user, **params)
    return tweet

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicTweetAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TWEETS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTweetApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username = 'username123',
            email = 'test@example.com',
            password = 'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_tweets(self):
        """Test retrieving a list of tweets."""
        create_tweet(user=self.user, tweet_text='test tweet')
        create_tweet(user=self.user, tweet_text='test tweet 2')

        res = self.client.get(TWEETS_URL)

        tweets = Tweet.objects.all().order_by('-id')
        serializer = TweetSerializer(tweets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tweet_list_limited_to_user(self):
        """Test list of tweets is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            username = 'othername123',
            email = 'other@example.com',
            password = 'otherpass123',
        )
        create_tweet(user=other_user, tweet_text='other tweet')
        create_tweet(user=self.user, tweet_text='this user')

        res = self.client.get(TWEETS_URL)

        tweets = Tweet.objects.filter(user=self.user)
        serializer = TweetSerializer(tweets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_tweet_detail(self):
        """Test get tweet detail."""
        tweet = create_tweet(user=self.user, tweet_text='detail tweet')

        url = detail_url(tweet.id)
        res = self.client.get(url)

        serializer = TweetDetailSerializer(tweet)
        self.assertEqual(res.data, serializer.data)

    def test_create_tweet(self):
        """Test creating a tweet."""
        payload = {'tweet_text': 'test tweet'}
        res = self.client.post(TWEETS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tweet = Tweet.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(tweet, k), v)
        self.assertEqual(tweet.user, self.user)

    def test_partial_update(self):
        """Test partial update of a tweet."""
        original_tweet = 'original tweet'
        tweet = create_tweet(user=self.user, tweet_text=original_tweet)

        payload = {'tweet_text': 'updated tweet'}
        url = detail_url(tweet.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tweet.refresh_from_db()
        self.assertEqual(tweet.tweet_text, payload['tweet_text'])
        self.assertEqual(tweet.user, self.user)

    def test_full_update(self):
        """Test full update of tweet."""
        tweet = create_tweet(user=self.user, tweet_text='test tweet')

        payload = {'tweet_text': 'updated tweet'}
        url = detail_url(tweet.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tweet.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(tweet, k), v)
        self.assertEqual(tweet.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the user of the tweet results in an error."""
        new_user = create_user(
            username = 'othername123',
            email = 'other@example.com',
            password = 'otherpass123',
        )
        tweet = create_tweet(user=self.user, tweet_text='test tweet')

        payload = {'user': new_user.id}
        url = detail_url(tweet.id)
        self.client.patch(url, payload)

        tweet.refresh_from_db()
        self.assertEqual(tweet.user, self.user)

    def test_delete_tweet(self):
        """Test deleting a tweet successful."""
        tweet = create_tweet(user=self.user, tweet_text='test tweet')
        url = detail_url(tweet.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tweet.objects.filter(id=tweet.id).exists())

    def test_recipe_other_users_recipe_error(self):
        """Test trying to delete another users tweet gives error."""
        new_user = create_user(
            username = 'othername123',
            email = 'other@example.com',
            password = 'otherpass123',
        )
        tweet = create_tweet(user=new_user, tweet_text='test tweet')

        url = detail_url(tweet.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Tweet.objects.filter(id=tweet.id).exists())