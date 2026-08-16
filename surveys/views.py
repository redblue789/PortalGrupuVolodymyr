from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import SurveyForm, build_page_form_class
from .models import Answer, Choice, Question, Survey, SurveyPage, SurveyResult
from .permissions import ModeratorRequiredMixin

SESSION_PREFIX = 'survey_answers_'


# ---------------------------------------------------------------------------
# Публічна частина: список опитувань та проходження
# ---------------------------------------------------------------------------

class SurveyListView(LoginRequiredMixin, ListView):
    model = Survey
    template_name = 'surveys/survey_list.html'
    context_object_name = 'surveys'

    def get_queryset(self):
        return Survey.objects.filter(is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        passed_ids = set(
            SurveyResult.objects.filter(user=self.request.user).values_list('survey_id', flat=True)
        )
        context['passed_ids'] = passed_ids
        return context


class SurveyDetailView(LoginRequiredMixin, DetailView):
    model = Survey
    template_name = 'surveys/survey_detail.html'
    context_object_name = 'survey'

    def get_queryset(self):
        return Survey.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['already_passed'] = SurveyResult.objects.filter(
            survey=self.object, user=self.request.user
        ).exists()
        return context


@login_required
def survey_take(request, slug, step=1):
    survey = get_object_or_404(Survey, slug=slug, is_active=True)
    pages = list(survey.pages.all())
    if not pages:
        messages.warning(request, 'Це опитування ще не готове (немає жодної сторінки з питаннями).')
        return redirect('surveys:detail', slug=survey.slug)

    total_steps = len(pages)
    if step < 1 or step > total_steps:
        return redirect('surveys:take', slug=survey.slug, step=1)

    page = pages[step - 1]
    session_key = f'{SESSION_PREFIX}{survey.pk}'
    session_data = request.session.get(session_key, {})

    form_class = build_page_form_class(page)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            session_data[str(page.pk)] = form.cleaned_data
            request.session[session_key] = session_data
            request.session.modified = True

            if step < total_steps:
                return redirect('surveys:take', slug=survey.slug, step=step + 1)
            return _finish_survey(request, survey, pages, session_data, session_key)
    else:
        initial = session_data.get(str(page.pk), {})
        form = form_class(initial=initial)

    context = {
        'survey': survey,
        'page': page,
        'form': form,
        'step': step,
        'total_steps': total_steps,
        'progress_percent': int(step / total_steps * 100),
        'has_previous': step > 1,
        'is_last_step': step == total_steps,
    }
    return render(request, 'surveys/survey_take.html', context)


def _finish_survey(request, survey, pages, session_data, session_key):
    """Зберігає (або перезаписує) результат проходження опитування."""
    result, created = SurveyResult.objects.get_or_create(survey=survey, user=request.user)
    if not created:
        result.answers.all().delete()
        result.save()  # оновлює passed_at (auto_now)

    for page in pages:
        page_answers = session_data.get(str(page.pk), {})
        for question in page.questions.all():
            value = page_answers.get(question.field_name)
            if value in (None, '', []):
                continue
            answer = Answer.objects.create(result=result, question=question)
            if question.question_type == Question.TEXT:
                answer.text_answer = value
                answer.save()
            elif question.question_type == Question.SINGLE:
                answer.choices.set(Choice.objects.filter(pk=value, question=question))
            else:
                answer.choices.set(Choice.objects.filter(pk__in=value, question=question))

    del request.session[session_key]
    request.session.modified = True
    messages.success(request, 'Дякуємо! Ваші відповіді збережено.')
    return redirect('surveys:thanks', slug=survey.slug)


@login_required
def survey_thanks(request, slug):
    survey = get_object_or_404(Survey, slug=slug)
    return render(request, 'surveys/survey_thanks.html', {'survey': survey})


# ---------------------------------------------------------------------------
# Модерація: створення / редагування / видалення опитувань, перегляд результатів
# ---------------------------------------------------------------------------

class ModerationSurveyListView(ModeratorRequiredMixin, ListView):
    model = Survey
    template_name = 'surveys/moderation_list.html'
    context_object_name = 'surveys'
    queryset = Survey.objects.all().order_by('-created_at')


class SurveyCreateView(ModeratorRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Опитування створено. Тепер додайте сторінки та питання нижче.',
        )
        return response

    def get_success_url(self):
        return reverse('admin:surveys_survey_change', args=[self.object.pk])


class SurveyUpdateView(ModeratorRequiredMixin, UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'

    def get_success_url(self):
        return reverse('surveys:moderation_list')


class SurveyDeleteView(ModeratorRequiredMixin, DeleteView):
    model = Survey
    template_name = 'surveys/survey_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, f'Опитування «{self.object.title}» видалено.')
        return reverse('surveys:moderation_list')


class SurveyResultsView(ModeratorRequiredMixin, DetailView):
    model = Survey
    template_name = 'surveys/survey_results.html'
    context_object_name = 'survey'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.object
        respondents_count = survey.results.count()

        questions_data = []
        for page in survey.pages.all():
            for question in page.questions.all():
                if question.question_type == Question.TEXT:
                    answers = Answer.objects.filter(
                        question=question
                    ).exclude(text_answer='').select_related('result__user')
                    questions_data.append({
                        'question': question,
                        'is_text': True,
                        'answers': answers,
                        'answers_count': answers.count(),
                    })
                else:
                    stats = []
                    for choice in question.choices.all():
                        count = choice.answers.filter(question=question).count()
                        percent = round(count / respondents_count * 100, 1) if respondents_count else 0
                        stats.append({'choice': choice, 'count': count, 'percent': percent})
                    questions_data.append({
                        'question': question,
                        'is_text': False,
                        'stats': stats,
                    })

        context['respondents_count'] = respondents_count
        context['questions_data'] = questions_data
        return context
