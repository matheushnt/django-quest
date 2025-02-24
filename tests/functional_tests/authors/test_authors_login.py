import pytest
from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        str_password = 'P@ssw0rd'
        user = User.objects.create_user(
            username='my_user',
            password=str_password,
        )

        url_login = reverse('authors:login')
        self.browser.get(self.live_server_url + url_login)

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')
        username_field.send_keys(user.username)
        password_field.send_keys(str_password)
        form.submit()

        body = self.get_body()
        msg_login = f'Your are logged in with {user.username}.'
        self.assertIn(msg_login, body)

    def test_login_create_raises_404_if_not_POST_method(self):
        url_login_create = reverse('authors:login_create')
        self.browser.get(self.live_server_url + url_login_create)

        body = self.get_body()
        self.assertIn('Not Found', body)

    def test_form_login_is_invalid(self):
        url_login = reverse('authors:login')
        self.browser.get(self.live_server_url + url_login)

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')
        username_field.send_keys(' ')
        password_field.send_keys(' ')
        form.submit()

        body = self.get_body()

        self.assertIn('Invalid username or password', body)
