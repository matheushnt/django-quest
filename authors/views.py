from django.shortcuts import render
from .forms import RegisterForm


def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    context = {
        'form': form,
    }

    return render(request, 'authors/pages/register.html', context)
