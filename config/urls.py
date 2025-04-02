from django.contrib import admin
from django.urls import path, include
from apps.users.views import profile_view

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),

    path('', include('apps.core.urls')),
    path('profile/', include('apps.users.urls')), 
    path('@<username>/', profile_view, name='profile'), 

    path("__reload__/", include("django_browser_reload.urls")),
]

# Only use in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)