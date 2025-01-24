from django.core.exceptions import ValidationError
from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(name='Category Testing')
        return super().setUp()

    def test_recipe_category_model_string_representation(self):
        new_name = 'New Category Name'
        self.category.name = new_name
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), new_name)

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 70
        with self.assertRaises(ValidationError):
            self.category.full_clean()
