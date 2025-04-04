from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from .forms import *

# Create your views here.
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect('account_login')
    return render(request, 'profile.html', {'profile': profile})


@login_required
def profile_settings_view(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        messages.success(request, 'Post request received!')

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            # Add form errors to messages
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"User {field}: {error}")
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"Profile {field}: {error}")
    else:
        # For GET requests, show forms with current data
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile_settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def profile_password_change_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in
            messages.success(request, 'Password Update Successfully!')
            return redirect('settings')

    return render(request, 'password.html', {'form': form})

@login_required
def profile_email_change_view(request):
    user = request.user
    form = EmailForm(instance=user)

    if request.method == "POST":
        form = EmailForm(request.POST, instance=user)

        if form.is_valid():
            email = form.cleaned_data["email"]

            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.warning(request, f"{email} is already in use.")
            else:
                form.save()
                send_email_confirmation(request, user)
                messages.success(request, "Email updated! Please confirm your new email.")
            
            return redirect("profile-settings")

        messages.error(request, "Invalid email. Please try again.")

    return render(request, "email.html", {"form": form})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted!')
        return redirect('home')

    return render(request, 'account_delete.html')

def profile_email_verify_view(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')