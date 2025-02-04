from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm


def register(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)

    context = {
        'form': form,
    }

    return render(request, 'authors/pages/register.html', context)


def create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    return redirect('authors:register')
