from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import CreateUserView, ManageUserView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("tokens/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("tokens/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
