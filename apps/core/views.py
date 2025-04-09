from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext as _
from apps.users.forms import ThemeForm

def home_view(request):
    return render(request, "home.html")

def settings_view(request):
    return render(request, 'settings.html')

def settings_general_view(request):
    return render(request, 'settings/settings_general.html')

def settings_theme_view(request):
    if request.htmx:
        form = ThemeForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            theme = form.cleaned_data.get('theme')
            form.save()
            return JsonResponse({"success": True, "message": _("Theme updated successfully!")})
        return JsonResponse({"success": False, "message": _("Invalid theme selection")}, status=400)

    elif request.method == "POST":
        form = ThemeForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            theme = form.cleaned_data.get('theme')
            form.save()
            request.user.profile.theme = theme
            request.user.profile.save()

            messages.success(request, _("Theme switched to %(theme)s!") % {'theme': theme})
            return redirect("settings")
        else:
            messages.error(request, _("There was an issue with the theme selection."))
            return redirect('settings')

    form = ThemeForm(instance=request.user.profile) if request.user.is_authenticated else None
    return render(request, 'settings/settings_theme.html', {'form': form})
