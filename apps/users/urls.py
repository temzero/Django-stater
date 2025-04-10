from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_view, name="profile"),
    path("edit/", views.profile_edit_view, name="profile-edit"),
    path('password/', views.profile_password_change_view, name='profile-password-change'),
    path('email/', views.profile_email_change_view, name='profile-email-change'),
    path('emailverify/', views.profile_email_verify_view, name='profile-email-verify'),
    path('delete/', views.profile_delete_view, name='profile-delete'),
]
