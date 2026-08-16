"""
URL configuration for PortalGroup project.

The `urlpatterns` list routes URLs to views.

For more information please see:
https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

# Головна сторінка з основної гілки olegix7
from SuperSchool.views import home


urlpatterns = [
    # =========================
    # ОСНОВНИЙ САЙТ — olegix7
    # =========================

    # Головна сторінка
    path('', home, name='home'),

    # Адмінка Django
    path('admin/', admin.site.urls),


    # =========================
    # ДОДАТКОВИЙ ФУНКЦІОНАЛ — MikoshJostar
    # =========================

    # Система опитувань
    path(
        'surveys/',
        include('surveys.urls', namespace='surveys')
    ),

    # Вхід
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(),
        name='login'
    ),

    # Вихід
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),
]