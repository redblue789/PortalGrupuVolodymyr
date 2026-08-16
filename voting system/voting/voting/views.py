from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.db import transaction

from .models import Vote, VoteOption, UserVote
from .forms import VoteForm, VoteOptionFormSet, CastVoteForm


# ─── Міксини ────────────────────────────────────────────────────────────────

class AdminOrModeratorMixin(UserPassesTestMixin):
    """Доступ лише для адміністраторів і модераторів"""
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and (u.is_staff or u.is_superuser)


# ─── Список голосувань ───────────────────────────────────────────────────────

class VoteListView(ListView):
    model = Vote
    template_name = 'voting/vote_list.html'
    context_object_name = 'votes'
    paginate_by = 10

    def get_queryset(self):
        # Звичайні користувачі бачать лише активні голосування
        qs = Vote.objects.prefetch_related('options')
        user = self.request.user
        if not (user.is_authenticated and (user.is_staff or user.is_superuser)):
            qs = qs.filter(is_active=True)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Які голосування вже пройшов цей користувач
            voted_ids = UserVote.objects.filter(
                user=self.request.user
            ).values_list('option__vote_id', flat=True).distinct()
            ctx['voted_ids'] = set(voted_ids)
        else:
            ctx['voted_ids'] = set()
        return ctx


# ─── Деталі / результати голосування ────────────────────────────────────────

class VoteDetailView(DetailView):
    model = Vote
    template_name = 'voting/vote_detail.html'
    context_object_name = 'vote'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        vote = self.get_object()
        user = self.request.user

        user_vote = None
        if user.is_authenticated:
            user_vote = UserVote.objects.filter(
                user=user, option__vote=vote
            ).select_related('option').first()

        ctx['user_vote'] = user_vote
        ctx['form'] = CastVoteForm(vote) if (user.is_authenticated and not user_vote) else None
        ctx['options_with_stats'] = [
            {
                'option': opt,
                'count': opt.vote_count(),
                'percent': opt.vote_percent(),
            }
            for opt in vote.options.all()
        ]
        return ctx


# ─── Проголосувати ───────────────────────────────────────────────────────────

class CastVoteView(LoginRequiredMixin, View):
    """POST: зареєстрований користувач голосує (або переголосовує)"""

    def post(self, request, pk):
        vote = get_object_or_404(Vote, pk=pk, is_active=True)
        form = CastVoteForm(vote, request.POST)

        if form.is_valid():
            selected_option = form.cleaned_data['option']
            with transaction.atomic():
                # Видаляємо попередній голос якщо є → зберігається лише останній
                UserVote.objects.filter(user=request.user, option__vote=vote).delete()
                UserVote.objects.create(user=request.user, option=selected_option)
            messages.success(request, "Ваш голос прийнято!")
        else:
            messages.error(request, "Будь ласка, оберіть варіант.")

        return redirect('voting:vote_detail', pk=pk)


# ─── Створення голосування ───────────────────────────────────────────────────

class VoteCreateView(AdminOrModeratorMixin, CreateView):
    model = Vote
    form_class = VoteForm
    template_name = 'voting/vote_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['option_formset'] = VoteOptionFormSet(self.request.POST)
        else:
            ctx['option_formset'] = VoteOptionFormSet()
        ctx['form_title'] = 'Створити голосування'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        option_formset = ctx['option_formset']

        if option_formset.is_valid():
            with transaction.atomic():
                form.instance.created_by = self.request.user
                self.object = form.save()
                option_formset.instance = self.object
                option_formset.save()
            messages.success(self.request, "Голосування створено!")
            return redirect('voting:vote_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))


# ─── Редагування голосування ─────────────────────────────────────────────────

class VoteUpdateView(AdminOrModeratorMixin, UpdateView):
    model = Vote
    form_class = VoteForm
    template_name = 'voting/vote_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['option_formset'] = VoteOptionFormSet(self.request.POST, instance=self.object)
        else:
            ctx['option_formset'] = VoteOptionFormSet(instance=self.object)
        ctx['form_title'] = 'Редагувати голосування'
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        option_formset = ctx['option_formset']

        if option_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                option_formset.instance = self.object
                option_formset.save()
            messages.success(self.request, "Голосування оновлено!")
            return redirect('voting:vote_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))


# ─── Видалення голосування ───────────────────────────────────────────────────

class VoteDeleteView(AdminOrModeratorMixin, DeleteView):
    model = Vote
    template_name = 'voting/vote_confirm_delete.html'
    success_url = reverse_lazy('voting:vote_list')
    context_object_name = 'vote'

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Голосування видалено.")
        return super().delete(request, *args, **kwargs)
