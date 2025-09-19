"""
This is the Serializer Class for the Custom User Model
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from utils.choices import CLIENT_ROLES, TEAM_ROLES
User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """  Serializer for Custom User Model """
    # pylint: disable=too-few-public-methods
    class Meta:
        """  Meta class for CustomUserSerializer """
        model = User
        fields = ['id', 'email', 'role', 'is_active', 'is_staff']
        read_only_fields = ['id', 'email']


class ClientRoleUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for Client Roles """
    # pylint: disable=too-few-public-methods
    class Meta:
        """  Meta class for ClientRoleUpdateSerializer """
        model = User
        fields = ['role']

    def validate_role(self, value):
        """ Validate role """
        if value not in CLIENT_ROLES:
            raise serializers.ValidationError(
                "Role must be Student, Tutor, or Parent")
        return value


class TeamRoleUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for Team Roles """
    # pylint: disable=too-few-public-methods
    class Meta:
        """  Meta class for ClientRoleUpdateSerializer """
        model = User
        fields = ['role']

    def validate_role(self, value):
        """  Validate role """
        if value not in TEAM_ROLES:
            raise serializers.ValidationError(
                "Role must be Admin, Operations, HeadOfDepartment, Finance, or Sales")
        return value
