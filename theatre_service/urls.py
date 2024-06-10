"""
URL configuration for theatre_service project.
"""

from django.contrib import admin
from django.urls import path, include

from theatre_service import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/theatre/", include("theatre.urls", namespace="theatre")),
    path("api/user/", include("user.urls", namespace="user")),
]

if settings.DEV_MODE:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
