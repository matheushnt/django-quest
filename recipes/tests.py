from django.test import TestCase
from django.urls import reverse


# Create your tests here.


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
