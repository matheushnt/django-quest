from django.contrib import admin
from .models import Category, Recipe

# Register your models here.

# Primeira maneira de se registrar um model


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)

# Segunda maneira de se registrar um model


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...
