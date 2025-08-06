from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Profile, Auther


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'phone_number', 'address']
        read_only_fields = ['id']

class AutherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auther
        fields = ['id', 'user', 'bio', 'profile_picture', 'website', 'social_links']
        read_only_fields = ['id']
