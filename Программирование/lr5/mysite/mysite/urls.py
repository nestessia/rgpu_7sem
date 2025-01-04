from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('users/', include('users.urls')),
    path('api/', include([
        path('polls/', include('polls_api.urls')),
        path('export/', include('polls_export.urls')),
    ])),
]