from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr, is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__errors_form = {}

        add_attr(self.fields.get('preparation_step'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_step',
            'cover',
        ]

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self):
        super().clean()
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title and len(title) < 5:
            self.__errors_form.setdefault('title', []).append(
                'Must have at least 5 chars')

        if title == description:
            self.__errors_form.setdefault('title', []).append(
                'Cannot be equal to description'
            )
            self.__errors_form.setdefault('description', []).append(
                'Cannot be equal to title'
            )

        if self.__errors_form:
            raise ValidationError(self.__errors_form)

        return cleaned_data

    def clean_preparation_time(self):
        field_value = self.cleaned_data.get('preparation_time')

        if not is_positive_number(field_value):
            self.__errors_form.setdefault('preparation_time', []).append(
                'Must be a positive number'
            )

        return field_value

    def clean_servings(self):
        field_value = self.cleaned_data.get('servings')

        if not is_positive_number(field_value):
            self.__errors_form.setdefault('servings', []).append(
                'Must be a positive number'
            )

        return field_value
