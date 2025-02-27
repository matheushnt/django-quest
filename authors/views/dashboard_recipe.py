from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm


class DashboardRecipe(View):
    def get(self, request, id):
        recipe = Recipe.objects.filter(
            pk=id,
            is_published=False,
            author=request.user,
        ).first()

        if not recipe:
            raise Http404()

        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(
                request, 'Your recipe has been saved successfully')

            return redirect(
                reverse(
                    'authors:dashboard_recipe_edit',
                    args=(id,),
                )
            )

        context = {
            'form': form
        }

        return render(request, 'authors/pages/dashboard_recipe.html', context)
