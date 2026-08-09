from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('event/add/', views.event_create, name='event_add'),
    path('event/<int:pk>/edit/', views.event_update, name='event_edit'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
]
