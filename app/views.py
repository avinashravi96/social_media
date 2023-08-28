from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import User, FriendRequest
from .serializers import UserSignupSerializer, UserSerializer, FriendRequestSerializer, FriendsListSerialzer

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"user_id": user.id, "token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserSearchView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get(self, request):
        search_keyword = request.query_params.get('q', None)
        paginator = self.pagination_class()
        if search_keyword:
            users = User.objects.filter(email__iexact=search_keyword) | User.objects.filter(username__icontains=search_keyword)
            result_page = paginator.paginate_queryset(users, request)
            serializer = UserSerializer(result_page, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class FriendRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def post(self, request):
        from_user = request.user
        to_user_id = request.data.get('to_user_id')
        
        if FriendRequest.objects.filter(from_user=from_user, to_user_id=to_user_id).exists():
            return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship = FriendRequest(from_user=from_user, to_user_id=to_user_id, status='pending')
        friendship.save()
        return Response(status=status.HTTP_201_CREATED)

class FriendRequestUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, friendship_id):
        friendship = FriendRequest.objects.get(pk=friendship_id)
        if friendship.to_user != request.user:
            return Response({"detail": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        if new_status in ['accepted', 'rejected']:
            friendship.status = new_status
            friendship.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)
        
    

class FriendsListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        friendships = FriendRequest.objects.filter(status='accepted', from_user=user) | FriendRequest.objects.filter(status='accepted', to_user=user)
        serializer = FriendsListSerialzer(friendships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PendingFriendRequestsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user
        pending_requests = FriendRequest.objects.filter(to_user=user, status='pending')
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)