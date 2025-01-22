from django.test import TestCase
from recipes.models import Recipe, Category, User


class RecipeTestBase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(  # noqa: F841
            author=author,
            category=category,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutes',
            servings=5,
            servings_unit='Portions',
            preparation_step='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )

        return super().setUp()
