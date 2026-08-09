from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SuperSchool.urls')), # Підключаємо наш щоденник
]