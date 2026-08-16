from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Стандартні маршрути входу/виходу/зміни пароля Django
    # (login, logout, password_change, password_reset, ...)
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('events.urls')),
]
