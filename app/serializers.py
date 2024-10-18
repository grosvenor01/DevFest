from rest_framework import serializers
from .models import *

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} # the field will only be used for deserialization (when creating or updating an object
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = maintenance
        fields = "__all__"

class machineSerializer(serializers.ModelSerializer):
    class Meta:
        model = machine
        fields = "__all__"