from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/create/', views.create, name='create'),
]
