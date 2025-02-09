from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_value):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_value}'.strip()


def add_placeholder(field, attr_new_value):
    add_attr(field, 'placeholder', attr_new_value)


class RegisterForm(forms.ModelForm):
    # First way to overwrite fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['email'], 'Your e-mail')

    # Second way to overwrite fields
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'rquired': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password'
        })
    )

    # Third way to overwrite fields
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        # exclude = ['first_name']

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }

        help_texts = {
            'email': 'The e-mail must be valid.'
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty.',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here',
                'class': 'input text-input',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            }),
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Do not enter "%(value)s" in the password field',
                code='invalid',
                params={
                    'value': 'atenção'
                }
            )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            password_confirmation_error = ValidationError(
                'Passwords must be the same',
                code='invalid',
            )

            raise ValidationError({
                'password': 'Passwords must be the same',
                'confirm_password': [
                    password_confirmation_error,
                ],
            })
