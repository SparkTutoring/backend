"""  
This is the View for Accounts to change the default user model,
For Basic CRUD -> Team Members and GHL Webhooks for Tutors, Students and Parents
"""

import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from utils.choices import CLIENT_ROLES, TEAM_ROLES
from .serializers import CustomUserSerializer, ClientRoleUpdateSerializer, TeamRoleUpdateSerializer
User = get_user_model()

# Optional: set webhook secret in environment variables
WEBHOOK_SECRET = os.getenv('GHL_WEBHOOK_SECRET', 'my_ghl_secret')

# ---------- CRUD endpoints ----------


# --- List parents / clients ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_parents(request):
    """  List parents / clients """
    parents = User.objects.filter(role__in=CLIENT_ROLES)
    serializer = CustomUserSerializer(parents, many=True)
    return Response(serializer.data)

# --- List team members ---


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_team_members(request):
    """  List team members"""
    team = User.objects.filter(role__in=TEAM_ROLES)
    serializer = CustomUserSerializer(team, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    """Retrieve a single user"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    """Create a user manually"""
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_client_role(request, user_id):
    """Update role for Student, Tutor, or Parent"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClientRoleUpdateSerializer(
        user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Update team member roles ---


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_team_role(request, user_id):
    """Update role for Admin, Operations, HeadOfDepartment, Finance, or Sales"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeamRoleUpdateSerializer(
        user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    """Delete a user"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)


# ---------- GHL webhook endpoint ----------
@api_view(['POST'])
@permission_classes([AllowAny])
def ghl_webhook_create_user(request):
    """
    Endpoint to create users via GHL webhook
    Expects JSON payload:
    {
        "email": "parent@example.com",
        "role": "Parent"
    }
    """
    # Validate secret
    secret = request.headers.get('X-GHL-Webhook-Secret')
    if secret != WEBHOOK_SECRET:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    email = data.get('email')
    role = data.get('role', 'Parent')  # default role

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create or get user
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'role': role,
            'is_active': True,
        }
    )

    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
