from rest_framework import serializers
from .models import Story, CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class StorySerializer(serializers.ModelSerializer):
    # Custom field for the audio file URL
    audio_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ['id', 'title', 'text', 'audio_file', 'audio_file_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # can't be modified by the API

    def get_audio_file_url(self, obj):
        request = self.context.get('request')
        if obj.audio_file and hasattr(obj.audio_file, 'url'):
            # Use request.build_absolute_uri to construct the full URL
            return request.build_absolute_uri(obj.audio_file.url) if request else obj.audio_file.url
        return None


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'confirm_password')
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate_email(self, value):
        # Validate if the email is already in use
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Error occured while trying to create a user with this email.")
        return value

    def validate(self, data):
        # Check if the two passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "The two passwords differ."})
        return data

    def create(self, validated_data):
        # Remove the confirm_password field from the validated data
        validated_data.pop('confirm_password')
        
        # Create a new user instance with the validated data
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credential.")

        if not user.is_active:
            raise serializers.ValidationError("User is deactivated.")

        return user