from rest_framework import serializers

from users.models import Profile
from .models import Message, FriendTable, ContactRequest


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.PrimaryKeyRelatedField(source='sender', queryset=Profile.objects.all())
    receiver_id = serializers.PrimaryKeyRelatedField(source='receiver', queryset=Profile.objects.all())
    message = serializers.CharField(source='message')

    class Meta:
        model = Message
        fields = ['sender_id', 'receiver_id', 'message']


class FriendTableSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(source='user', queryset=Profile.objects.all())
    friend_id = serializers.PrimaryKeyRelatedField(source='friend', queryset=Profile.objects.all())

    class Meta:
        model = FriendTable
        fields = ['owner_id', 'friend_id']


class ContactRequestSerializer(serializers.ModelSerializer):
    requester = serializers.PrimaryKeyRelatedField(source='user', queryset=Profile.objects.all())
    pending_friend = serializers.PrimaryKeyRelatedField(source='friend', queryset=Profile.objects.all())
    status = serializers.IntegerField(required=False)
    class Meta:
        model = ContactRequest
        fields = ['requester', 'pending_friend', 'status']