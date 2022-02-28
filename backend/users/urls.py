from django.urls import include, path

from .views import Me, ListUsers, RegisterUser
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path(route="me", view=Me.as_view(), name="me"),
    path(route="users", view=ListUsers.as_view(), name="user_list"),
    path(route="register", view=RegisterUser.as_view(), name="user_register"),
    path(route="auth-token",  view=ObtainAuthToken.as_view(), name='user_token'),
    path("auth/", include("dj_rest_auth.urls")),
]