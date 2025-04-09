from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import *

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

        messages.success(request, _('Post request received!'))

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Profile updated successfully!'))
            return redirect('profile')
        else:
            # Add form errors to messages
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, _("User %(field)s: %(error)s") % {'field': field, 'error': error})
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, _("Profile %(field)s: %(error)s") % {'field': field, 'error': error})
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile_settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.urls import reverse

@login_required
def profile_password_change_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)

    if request.htmx:
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, _('Password updated successfully!'))
            response = HttpResponse()
            response["HX-Redirect"] = reverse("settings")
            return response
        else:
            return render(request, 'partials/password_errors.html', {'form': form})

    elif request.method == "POST":
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, _('Password changed!'))
            return redirect('settings')

    return render(request, 'change_password.html', {'form': form})

@login_required
def profile_email_change_view(request):
    user = request.user
    form = EmailForm(instance=user)

    if request.method == "POST":
        form = EmailForm(request.POST, instance=user)

        if form.is_valid():
            email = form.cleaned_data["email"]

            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.warning(request, _("%(email)s is already in use.") % {'email': email})
            else:
                form.save()
                send_email_confirmation(request, user)
                messages.success(request, _("Email updated! Please confirm your new email."))

            return redirect("profile-settings")

        messages.error(request, _("Invalid email. Please try again."))

    return render(request, "email.html", {"form": form})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, _('Account deleted!'))
        return redirect('home')

    return render(request, 'account_delete.html')

@login_required
def profile_email_verify_view(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')
