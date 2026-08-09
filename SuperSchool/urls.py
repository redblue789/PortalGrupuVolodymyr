from django.urls import path
from . import views

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('thread/<int:pk>/', views.thread_detail, name='thread_detail'),
    path('thread/new/', views.create_thread, name='create_thread'),
    path('thread/<int:pk>/edit/', views.edit_thread, name='edit_thread'),
    path('thread/<int:pk>/delete/', views.delete_thread, name='delete_thread'),
]