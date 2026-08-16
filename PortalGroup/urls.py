from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from SuperSchool.views import home

urlpatterns = [
    path('',         home,                                          name='home'),
    path('admin/',   admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('forum/',   include(('SuperSchool.urls', 'forum'), namespace='forum')),
    path('events/',  include('events.urls')),
]
