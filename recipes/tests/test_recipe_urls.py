from django.test import TestCase
from django.urls import reverse
import pytest


@pytest.mark.fast
class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('recipes:recipe', args=(1,))
        self.assertEqual('/recipes/1/', url)

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual('/recipes/category/1/', url)

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
