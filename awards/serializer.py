from rest_framework import serializers
from .models import Profile, Project
from django.contrib.auth.models import User

# profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("user", "profile_photo", "bio", "contact")


# Project serializer
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("user", "title", "description", "image", "url", "location", "date")

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    project = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'profile', 'posts']