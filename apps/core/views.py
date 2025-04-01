from django.shortcuts import render
from django.contrib import messages


def home_view(request):
    messages.error(request, 'There was an error while saving your changes.')
    messages.warning(request, 'Be careful, something might go wrong.')
    messages.success(request, 'Your changes were saved successfully!')
    messages.info(request, 'This is an informational message.')
    return render(request, "home.html")

def settings_view(request):
    return render (request, 'settings.html')

def settings_general_view(request):
    return render (request, 'settings_general.html')