import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(
            self.fields['confirm_password'], 'Repeat your password')

    first_name = forms.CharField(
        label='First name',
        error_messages={
            'required': 'Type your first name'
        },
    )

    last_name = forms.CharField(
        label='Last name',
        error_messages={
            'required': 'Type your last name'
        },
    )

    username = forms.CharField(
        label='Username',
        min_length=4,
        max_length=150,
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have at most 150 characters',
        },
        help_text=(
            'Username must have letters, '
            'numbers and one of those: @, ., +, -, _. '
            'The lenght should be between 4 and 150 characters.'
        ),
    )

    email = forms.CharField(
        label='Email',
        error_messages={
            'required': 'E-mail is required'
        },
        help_text='The e-mail must be valid.',
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        label='Password',
        validators=[strong_password]
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirm password',
        error_messages={
            'required': 'Please, repeat your password'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(value)s no campo password',
                code='invalid',
                params={'value': '"atenção"'}
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': '"John Doe"'}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_confirmation_error = ValidationError(
                'Passwords must be the same',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'confirm_password': [
                    password_confirmation_error,
                ],
            })
