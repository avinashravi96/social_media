from django.urls import path 
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserSignupView, UserSearchView, FriendRequestView, FriendRequestUpdate, FriendsListView, PendingFriendRequestsView

urlpatterns = [
    path('api/signup', UserSignupView.as_view(), name='user-signup'),
    path('api/login', obtain_auth_token, name='user-login'),
    path('api/users/search', UserSearchView.as_view(), name='user-search'),
    path('api/friend-requests', FriendRequestView.as_view(), name='send-friend-request'),
    path('api/pending-friend-requests', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
    path('api/friend-requests-update/<int:friendship_id>', FriendRequestUpdate.as_view(), name='accept-reject-friend-request'),
    path('api/friends', FriendsListView.as_view(), name='friend-list')
]