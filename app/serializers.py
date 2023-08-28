from rest_framework import serializers
from .models import User, FriendRequest

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class FriendRequestSerializer(serializers.ModelSerializer):
    sent_user_data = UserSerializer(source='from_user', read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['id', 'sent_user_data', 'status', 'created_at', 'updated_at']

class FriendsListSerialzer(serializers.ModelSerializer):
    friend_data =  UserSerializer(source='from_user', read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['id', 'friend_data', 'created_at', 'updated_at']
