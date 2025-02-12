from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('confirm_password', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('email', 'The e-mail must be valid.'),
        ('username', (
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.'
        )),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('confirm_password', 'Confirm password'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(needed, current)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            'first_name': 'Will',
            'last_name': 'Sant',
            'username': 'willsant',
            'email': 'ws@email.com',
            'password': 'WStrong@123',
            'confirm_password': 'WStrong@123',
        }

        return super().setUp()

    @parameterized.expand([
        ('username', 'This field must not be empty')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertContains(response, msg, html=True)
