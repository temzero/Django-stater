from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext as _

def home_view(request):
    # messages.error(request, 'errorerrorerror')
    # messages.success(request, 'success')
    # messages.warning(request, 'warning')
    # messages.info(request, 'information')
    return render(request, "home.html")

def favorite_view(request):
    return render(request, 'favorite.html')

def search_view(request):
    return render(request, 'search.html')

def settings_view(request):
    return render(request, 'settings.html')

def settings_general_view(request):
    return render(request, 'settings/settings_general.html')
