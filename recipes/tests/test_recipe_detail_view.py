from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
import pytest


@pytest.mark.fast
class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.RecipeDetailView)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        # Need a recipe for this test
        needed_title = 'This is a detail page - It load one recipe'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_detail_template_wont_load_recipe_not_published(self):
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={
                    'pk': recipe.pk
                }
            )
        )

        self.assertEqual(response.status_code, 404)
