from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('favorite/', favorite_view, name='favorite'),
    path('search/', search_view, name='search'),
    path('settings/', settings_view, name='settings'),
    path('settings/general', settings_general_view, name='settings-general'),
]
