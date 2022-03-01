from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .utils import make_user, get_user, get_user_token


class TestUserAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_user(username="bob")
        cls.url = reverse(viewname="user_list")

    def test_allows_authenticated_user_to_get_users(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], self.user.username)

    def test_denies_unauthenticated_user_to_get_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestMeAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_user(username="bob")
        cls.url = reverse(viewname="me")

    def test_return_own_information(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["username"], self.user.username)

    def test_does_not_return_information_to_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestRegisterAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_user(username="bob")
        cls.register_url = reverse(viewname="user_register")
        cls.authtoken_url = reverse(viewname="user_token")

    def test_register_user(self):
        response = self.client.post(self.register_url, {"username":"bobby", "password" : "pass"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "bobby")

    def test_register_does_not_create_superuser_or_staff_user(self):
        response = self.client.post(self.register_url, {"username":"bobby2", "password" : "pass", "is_superuser" : True, "is_staff" : True})
        user = get_user(id=response.data['id'])
        self.assertEqual( getattr(user, 'is_superuser') , False)
        self.assertEqual(user.is_staff, False)

    def test_user_get_correct_authtoken_by_credentials(self):
        self.test_register_user()
        response = self.client.post(self.authtoken_url, {"username":"bobby", "password" : "pass"})
        t = [response.data["token"] for x in Token.objects.all()]
        self.assertEqual( response.data["token"] in t, True)

    def test_user_get_no_authtoken_by_wrong_credentials(self):
        self.test_register_user()
        response = self.client.post(self.authtoken_url, {"username":"bobby", "password" : "wrong"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
