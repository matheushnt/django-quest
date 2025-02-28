import os

from django.http import Http404
from django.db.models import Q
from django.views.generic import DetailView
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

        if not queryset:
            raise Http404()

        return queryset

    def get_context_data(self):
        context = super().get_context_data()

        context.update({
            'title': f'{context.get('recipes', None)[0].category.name}'
        })

        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        search_term = self.request.GET.get('q')

        if not search_term:
            raise Http404()

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


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'is_detail_page': True
        })

        return context
