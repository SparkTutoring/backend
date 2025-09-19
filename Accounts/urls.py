"""  
This is the URLs for Accounts to change the default user model,
For Basic CRUD -> Team Members and GHL Webhooks for Tutors, Students and Parents"""

from django.urls import path
from . import views

# pylint: disable=invalid-name
app_name = 'accounts'

urlpatterns = [
    # --- CRUD for users ---
    # List parents / clients
    path('parents/', views.list_parents, name='list-parents'),
    path('team-members/', views.list_team_members,
         name='list-team-members'),  # List team members
    path('users/<int:user_id>/', views.get_user,
         name='get-user'),       # Get single user
    path('users/create/', views.create_user,
         name='create-user'),        # Create user manually
    path('users/<int:user_id>/delete/', views.delete_user,
         name='delete-user'),  # Delete user

    # --- Role updates ---
    path('users/<int:user_id>/client-role/',
         views.update_client_role, name='update-client-role'),
    path('users/<int:user_id>/team-role/',
         views.update_team_role, name='update-team-role'),

    # --- GHL webhook ---
    path('webhook/ghl/', views.ghl_webhook_create_user,
         name='ghl-webhook-create-user'),
]
