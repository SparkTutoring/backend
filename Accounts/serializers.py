"""
This is the Serializer Class for the Custom User Model
"""
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for the CustomUser model """
    # pylint: disable=too-few-public-methods
    class Meta:
        """ Meta class for CustomUserSerializer """
        model = CustomUser
        fields = ['id', 'email', 'role', 'is_active', 'is_staff']
        read_only_fields = ['id', 'is_staff']
