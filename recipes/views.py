import os

from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.views.generic.list import ListView
from utils.pagination import make_pagination
from .models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            is_published=True,
        )

        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )

        context.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )

        return context


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True,
        ).order_by('-id')

        return queryset

    def get_context_data(self):
        context = super().get_context_data()

        page_obj, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGE
        )

        context.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )

        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        search_term = self.request.GET.get('q')

        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True
        ).order_by('-id')

        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        search_term = self.request.GET.get('q')

        context.update(
            {
                'page_title': f'Search for "{search_term}" | ',
                'search_term': search_term,
                'additional_url_query': f'&q={search_term}',
            }
        )

        return context


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGE,
    )

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGE,
    )

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category | ',
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True

    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGE,
    )

    context = {
        'page_title': f'Search for "{search_term}" | ',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    }

    return render(request, 'recipes/pages/search.html', context)
