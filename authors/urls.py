from django.urls import path
from . import views

app_name = 'authors'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create_view,
         name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create_view, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
]
