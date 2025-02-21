from .test_recipe_base import RecipeTestBase
from django.urls import reverse
import pytest


@pytest.mark.slow
class PaginationTest(RecipeTestBase):
    def make_recipes(self, qty_recipes):
        for i in range(qty_recipes):
            self.make_recipe(
                author={'username': f'username{i}'},
                title=f'Recipe {i}',
                slug=f'slug-diff-{i}'
            )

    def test_recipe_maximum_home_recipes_per_page(self):
        self.make_recipes(30)

        url = reverse('recipes:home')
        response = self.client.get(url)
        recipes = response.context['recipes']
        self.assertLessEqual(len(recipes), 9)

    def test_recipe_maximum_category_per_page(self):
        self.make_recipes(30)

        url = reverse('recipes:category', kwargs={'category_id': 1})
        response = self.client.get(url)
        recipes = response.context['recipes']
        self.assertLessEqual(len(recipes), 9)

    def test_recipe_maximum_search_per_page(self):
        title = 'Bolo de Avelã'

        for i in range(30):
            self.make_recipe(
                author={'username': f'username{i}'},
                title=title,
                slug=f'slug-diff-{i}'
            )

        url = reverse('recipes:search')
        response = self.client.get(f'{url}?q={title}')
        recipes = response.context['recipes']
        self.assertLessEqual(len(recipes), 9)
