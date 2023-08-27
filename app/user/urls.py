"""
URL mappings for the user API.
"""
from django.urls import path
from user import views


app_name = 'user'



urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('followings/', views.FollowViewSet.as_view({'get':'list'}), name='followings'),
    path('follow/', views.FollowViewSet.as_view({'post':'follow'}), name='follow'),
    path('unfollow/', views.FollowViewSet.as_view({'post':'unfollow'}), name='unfollow'),
    path('upload_image/', views.UploadProfilePictureView.as_view(), name='upload_image'),

]