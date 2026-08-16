from django.urls import path

from . import views

app_name = 'surveys'

urlpatterns = [
    # Публічна частина
    path('', views.SurveyListView.as_view(), name='list'),
    path('<slug:slug>/', views.SurveyDetailView.as_view(), name='detail'),
    path('<slug:slug>/take/', views.survey_take, {'step': 1}, name='take_start'),
    path('<slug:slug>/take/<int:step>/', views.survey_take, name='take'),
    path('<slug:slug>/thanks/', views.survey_thanks, name='thanks'),

    # Модерація (адміністратори/модератори)
    path('moderation/', views.ModerationSurveyListView.as_view(), name='moderation_list'),
    path('moderation/create/', views.SurveyCreateView.as_view(), name='create'),
    path('moderation/<slug:slug>/edit/', views.SurveyUpdateView.as_view(), name='edit'),
    path('moderation/<slug:slug>/delete/', views.SurveyDeleteView.as_view(), name='delete'),
    path('moderation/<slug:slug>/results/', views.SurveyResultsView.as_view(), name='results'),
]
