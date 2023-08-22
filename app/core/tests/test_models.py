"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        username = 'user123'
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            username = username,
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails=[
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for i, (email, expected) in enumerate(sample_emails, 0):
            username = f'user{i}'
            user = get_user_model().objects.create_user(username, email, 'pw123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('user123', '', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'superuser123',
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_tweet(self):
        """Test creating a tweet is successful."""
        user = get_user_model().objects.create_user(
            username = 'username123',
            email = 'test@example.com',
            password = 'testpass123',
        )
        tweet = models.Tweet.objects.create(
            user=user,
            tweet_text = 'My first Tweet.',
        )

        self.assertEqual(str(tweet), tweet.tweet_text)