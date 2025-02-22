from .base import RecipeBaseFunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
import pytest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 😭', body.text)

    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(10)
        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        self.browser.get(self.live_server_url)

        search_input = self.browser.find_element(
            By.XPATH,
            '/html/body/div[1]/div/form/input',
        )

        search_input.click()
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        body = self.browser.find_element(By.TAG_NAME, 'body').text

        self.assertIn(title_needed, body)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch(9)
        self.browser.get(self.live_server_url)

        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )

        page2.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
