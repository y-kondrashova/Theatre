"""
URL configuration for theatre_service project.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from theatre_service import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/theatre/", include("theatre.urls", namespace="theatre")),
    path("api/users/", include("user.urls", namespace="user")),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc"
    ),
]

if settings.DEV_MODE:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
