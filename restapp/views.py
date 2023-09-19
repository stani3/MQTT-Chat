from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restapp.serializers import ContactRequestSerializer
from users.views import to_base64_img
from restapp.models import FriendTable, ContactRequest, Message
from users.models import Profile

from itertools import chain


@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # If you are using authentication classes
@permission_classes([IsAuthenticated])  # If you are using permission classes
def get_friends(request):
    current_user = request.user  # Get the currently logged-in user
    profile = Profile.objects.get(user=current_user)
    # Query the Friendship model to get the user's friends
    friend_list = FriendTable.objects.filter(owner=profile)

    # Extract friend IDs and usernames
    friends_data = [{
        'id': contact.friend.id,
        'username': contact.friend.user.username,
        'email': contact.friend.user.email,
        'photo': to_base64_img(contact.friend),
        'name': contact.friend.name} for contact in friend_list]

    return Response({'friends': friends_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # If you are using authentication classes
@permission_classes([IsAuthenticated])  # If you are using permission classes
def contact_request(request):
    serializer = ContactRequestSerializer(data=request.data)
    if serializer.is_valid():
        d = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # If you are using authentication classes
@permission_classes([IsAuthenticated])  # If you are using permission classes
def contact_request_by_username(request, username):
    profile = Profile.objects.get(user=request.user)
    friend = Profile.objects.get(user=User.objects.get(username=username))
    if ContactRequest.objects.filter(requester=profile, pending_friend=friend, status=1).exists():
        return Response("already sent", status=status.HTTP_400_BAD_REQUEST)

    req = ContactRequest.objects.create(requester=profile, pending_friend=friend)

    return Response({"OK"}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_contact_request(request, requester_id):
    profile = Profile.objects.get(user=request.user)
    requester = Profile.objects.get(id=requester_id)

    try:

        contact_request = ContactRequest.objects.get(requester=requester, pending_friend=profile)

    except ContactRequest.DoesNotExist:
        return Response({'error': 'Contact request not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ContactRequestSerializer(contact_request, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        if contact_request.status == 2:
            FriendTable.objects.create(owner=contact_request.requester, friend=contact_request.pending_friend)
            FriendTable.objects.create(owner=contact_request.pending_friend, friend=contact_request.requester)
        elif contact_request.status == 3:
            contact_request.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # If you are using authentication classes
@permission_classes([IsAuthenticated])  # If you are using permission classes
def get_contact_requests(request):
    profile = Profile.objects.get(user=request.user)
    # Query the Friendship model to get the user's friends
    friend_list = ContactRequest.objects.filter(pending_friend=profile, status=1)

    # Extract friend IDs and usernames
    friends_data = [{
        'id': contact.requester.id,
        'username': contact.requester.user.username,
        'email': contact.requester.user.email,
        'photo': to_base64_img(contact.requester),
        'name': contact.requester.name} for contact in friend_list]

    return Response({'requests': friends_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # If you are using authentication classes
@permission_classes([IsAuthenticated])  # If you are using permission classes
def send_message(request):
    serializer = Message(data=request.data)
    if serializer.is_valid():
        d = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # If you are using authentication classes
@permission_classes([IsAuthenticated])  # If you are using permission classes
def get_chat(request, friend_id):
    current_user = request.user  # Get the currently logged-in user
    profile = Profile.objects.get(user=current_user)
    friend = Profile.objects.get(id=friend_id)
    # Query the Friendship model to get the user's friends
    messages = Message.objects.filter(sender=profile, receiver=friend)
    messages_2 = Message.objects.filter(sender=friend, receiver=profile)

    all_messages = chain(messages, messages_2)

    # Sort the combined queryset by date
    sorted_messages = sorted(all_messages, key=lambda message: message.date)
    message_dict = []
    for message in sorted_messages:
        message_item = {
            "id": message.id,
            "message": message.content,
            "timestamp": int(message.date.timestamp() * 1000),  # Convert to milliseconds
            "type": "text",
            "sent_received": "sent" if message.sender == profile else "received",
            "status": "sent" if message.status == 1 else "received"  # Adjust based on your actual logic
        }
        message_dict.append(message_item)
    #print(message_dict)
    return Response({'messages': message_dict}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # If you are using authentication classes
@permission_classes([IsAuthenticated])  # If you are using permission classes
def get_last_msg(request, friend_id):
    current_user = request.user  # Get the currently logged-in user
    profile = Profile.objects.get(user=current_user)
    friend = Profile.objects.get(id=friend_id)
    # Query the Friendship model to get the user's friends
    messages = Message.objects.filter(sender=profile, receiver=friend)
    messages_2 = Message.objects.filter(sender=friend, receiver=profile)
    if(messages.exists() or messages_2.exists()):

        all_messages = chain(messages, messages_2)

        # Sort the combined queryset by date
        sorted_messages = sorted(all_messages, key=lambda message: message.date)

        message = sorted_messages[0]
        message_item = {
            "id": message.id,
            "message": message.content,
            "timestamp": int(message.date.timestamp() * 1000),  # Convert to milliseconds
            "type": "text",
            "sent_received": "sent" if message.sender == profile else "received",
            "status": "sent" if message.status == 1 else "received"  # Adjust based on your actual logic
        }

        #print(message_item)
        return Response(message_item, status=status.HTTP_200_OK)
    else:
        return Response({}, status=status.HTTP_404_NOT_FOUND)