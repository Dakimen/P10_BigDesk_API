"""
This module contains serializers
relevant to user creation and authentication in custom_auth application.
"""
from rest_framework import serializers

from custom_auth.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'age',
                  'can_be_contacted', 'can_data_be_shared']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            age=validated_data['age'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared'],
        )
        return user
