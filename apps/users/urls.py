from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_view, name="profile"),
    path("settings/", views.profile_settings_view, name="profile-settings"),
    path('password/', views.profile_password_change_view, name='profile-password-change'),
    path('email/', views.profile_email_change_view, name='profile-email-change'),
    path('emailverify/', views.profile_email_verify_view, name='profile-email-verify'),
    path('delete/', views.profile_delete_view, name='profile-delete'),
]
