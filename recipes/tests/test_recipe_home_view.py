from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_not_found_recipes_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here 😭</h1>',
            response.content.decode('utf-8'),
        )

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_template_wont_load_recipes_not_published(self):
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('<h1>No recipes found here 😭</h1>', content)

        url = reverse('recipes:search') + '?q=Receita de bolo'
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn('Search for &quot;Receita de bolo&quot; | ', content)

    # @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_is_paginated(self):
        for i in range(10):
            kwargs = {
                'slug': f'slug-diff{i}',
                'author': {
                    'username': f'usernm{i}'
                }
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            url = reverse('recipes:home')
            response = self.client.get(url)
            recipes = response.context['recipes']
            paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 4)
        self.assertLessEqual(len(paginator.get_page(1)), 3)
        self.assertLessEqual(len(paginator.get_page(2)), 3)
        self.assertLessEqual(len(paginator.get_page(3)), 3)
        self.assertLessEqual(len(paginator.get_page(4)), 3)
