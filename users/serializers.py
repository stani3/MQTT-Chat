from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile  # Import your Profile model

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15)  # Adjust the max_length as needed
    name = serializers.CharField(max_length=150, required=False)  # Allow 'name' but not required
    photo = serializers.ImageField(required=False)  # Allow 'photo' but not required
    def create(self, validated_data):
        # Extract the phone number from validated_data

        phone = validated_data.pop('phone')
        # Create a new user (excluding the 'phone' field)

        user = User.objects.create_user(**validated_data)

        # Create a profile for the user with the phone number
        profile = Profile.objects.get(user=user)
        profile.phone = phone
        profile.save()
        validated_data['phone'] = phone

        return validated_data
