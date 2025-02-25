from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
import pytest


@pytest.mark.fast
class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_view_funtion_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=testing')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=Receita de bolo'
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn('Search for &quot;Receita de bolo&quot; | ', content)

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        self.make_recipe(
            author={'username': 'one'},
            slug='one',
            title=title1,
        )
        self.make_recipe(
            author={'username': 'two'},
            slug='two',
            title=title2,
        )

        url = reverse('recipes:search')
        response1 = self.client.get(f'{url}?q={title1}')
        response2 = self.client.get(f'{url}?q={title2}')
        response_both = self.client.get(url + '?q=this')

        self.assertIn(title1, response1.content.decode('utf-8'))
        self.assertNotIn(title2, response1.content.decode('utf-8'))

        self.assertIn(title2, response2.content.decode('utf-8'))
        self.assertNotIn(title1, response2.content.decode('utf-8'))

        self.assertIn('this', response_both.content.decode('utf-8'))

        # It is possible to make assertions through context of the response
