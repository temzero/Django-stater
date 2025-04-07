from django.shortcuts import render, redirect
from django.contrib import messages
from apps.users.forms import ThemeForm
from django.contrib.auth.decorators import login_required


def home_view(request):
    # messages.info(request, 'This is an informational message.')
    # messages.error(request, 'There was an error while saving your changes.')
    # messages.warning(request, 'Be careful, something might go wrong.')
    # messages.success(request, 'Your changes were saved successfully!')
    return render(request, "home.html")

def settings_view(request):
    return render (request, 'settings.html')

def settings_general_view(request):
    return render (request, 'settings/settings_general.html')

def settings_theme_view(request):
    if request.htmx:
        form = ThemeForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            theme = form.cleaned_data.get('theme')
            form.save()

            return JsonResponse({"success": True, "message": "Theme updated successfully!"})
        # If the form is invalid, return a JSON error response
        return JsonResponse({"success": False, "message": "Invalid theme selection"}, status=400)

    elif request.method == "POST":  # Default behavior for non-HTMX requests (normal form submit)
        form = ThemeForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            theme = form.cleaned_data.get('theme')
            form.save()
            request.user.profile.theme = theme
            request.user.profile.save()

            messages.success(request, f"Theme switch to {theme}!")
            return redirect("settings-general")
        else:
            messages.error(request, "There was an issue with the theme selection.")
            return redirect('settings-general')


    # Render the form for GET requests
    # messages.warning(request, 'Be careful, something might go wrong.')
    # messages.success(request, 'Your changes were saved successfully!')
    # messages.error(request, 'There was an error while saving your changes.')
    # messages.info(request, 'This is an informational message.')
    form = ThemeForm(instance=request.user.profile)
    return render(request, 'settings/settings_theme.html', {'form': form})
