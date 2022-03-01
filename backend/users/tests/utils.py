from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

def make_user(username: str = "bob"):
    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(username=username, password="pass")
    return user

def get_user(id: int):
    user_model = get_user_model()
    return user_model.objects.get(id=id)

def get_user_token(id: int):
    user = get_user(id)
    return Token.objects.create(user=user).key