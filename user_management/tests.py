from django.test import TestCase
from django.urls import reverse_lazy

from user_management.models import CustomUser


# Create your tests here.
class TestUserView(TestCase):

    def setUp(self):
        email = "test@email.com"
        username = "test8"
        first_name = "testin"
        last_name = "testina"
        password = "testtest"
        self.u = CustomUser.objects.create_user(email=email, username=username, first_name=first_name,
                                                last_name=last_name, password=password)

    def login_user(self):
        self.client.login(email='test@email.com', password="testtest")

    def test_login_redirect(self):
        self.login_user()
        response = self.client.get(reverse_lazy('user_management:login'))
        self.assertEqual(response.status_code, 200, "Authenticated user should return 200")

    def test_user_account_view_logged_in(self):
        self.login_user()
        response = self.client.get(reverse_lazy('user_management:profile'))
        self.assertEqual(response.status_code, 200, 'User is logged in successfully')

    def test_user_account_view_not_logged_in(self):
        response = self.client.get(reverse_lazy('user_management:profile'))
        self.assertEqual(response.status_code, 302, 'User not logged in should be redirected')


