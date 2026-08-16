from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    # Список усіх голосувань
    path('', views.VoteListView.as_view(), name='vote_list'),

    # Деталі + результати конкретного голосування
    path('<int:pk>/', views.VoteDetailView.as_view(), name='vote_detail'),

    # Проголосувати (POST)
    path('<int:pk>/cast/', views.CastVoteView.as_view(), name='cast_vote'),

    # CRUD (лише адмін/модератор)
    path('create/', views.VoteCreateView.as_view(), name='vote_create'),
    path('<int:pk>/edit/', views.VoteUpdateView.as_view(), name='vote_update'),
    path('<int:pk>/delete/', views.VoteDeleteView.as_view(), name='vote_delete'),
]
