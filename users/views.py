import base64

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Profile
from .serializers import UserRegistrationSerializer





@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def verify_auth_token(request):
    return Response({"message": "Authentication successful"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user (anonymous) to create a new user
def create_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        d = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])  # Use POST for a logout request
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  # Require authentication to access this view
def logout_view(request):
    # Perform logout logic
    logout(request)
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_token(request):
    # The user associated with the token is available via request.user
    user = request.user

    profile = Profile.objects.get(user=user)
    image_base64 = to_base64_img(profile)
    return Response({
        'id': profile.id,
        'name': profile.name,
        'username': user.username,
        'email': user.email,
        'phone': profile.phone,
        'photo': image_base64,
    })


def to_base64_img(profile):
    image_base64 = None
    if profile.photo:
        # Open and read the image file
        with profile.photo.open("rb") as f:
            image_data = f.read()

        # Convert the image data to base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")
    return image_base64


@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:

        profile = Profile.objects.get(id=user_id)
        image_base64 = None
        if profile.photo:
            # Open and read the image file
            with profile.photo.open("rb") as f:
                image_data = f.read()

            # Convert the image data to base64
            image_base64 = base64.b64encode(image_data).decode("utf-8")
        user_data = {
            'id': profile.id,
            'name': profile.name,
            'username': profile.user.username,
            'email': profile.user.email,
            'phone': profile.phone,
            'photo': image_base64,
            # Include other fields you want to expose
        }
        return Response(user_data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)