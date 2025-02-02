from django.shortcuts import render
from .forms import RegisterForm


def register(request):
    form = RegisterForm()
    context = {
        'form': form,
    }

    return render(request, 'authors/pages/register.html', context)
