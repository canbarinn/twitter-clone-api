"""
URL mappings for the tweet app.
"""
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from tweet import views

router = DefaultRouter()
router.register('tweets', views.TweetViewSet)

app_name = 'tweet'

urlpatterns = [
    path('', include(router.urls)),
]