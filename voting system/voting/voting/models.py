from django.db import models
from django.contrib.auth.models import User


class Vote(models.Model):
    """Голосування"""
    title = models.CharField(max_length=255, verbose_name="Назва голосування")
    description = models.TextField(blank=True, verbose_name="Опис")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_votes',
        verbose_name="Створив"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    is_active = models.BooleanField(default=True, verbose_name="Активне")

    class Meta:
        verbose_name = "Голосування"
        verbose_name_plural = "Голосування"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def total_votes(self):
        """Загальна кількість проголосованих"""
        return UserVote.objects.filter(option__vote=self).values('user').distinct().count()


class VoteOption(models.Model):
    """Варіант відповіді у голосуванні"""
    vote = models.ForeignKey(
        Vote,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name="Голосування"
    )
    text = models.CharField(max_length=255, verbose_name="Текст варіанту")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Варіант відповіді"
        verbose_name_plural = "Варіанти відповіді"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.vote.title} — {self.text}"

    def vote_count(self):
        """Кількість голосів за цей варіант"""
        return self.user_votes.count()

    def vote_percent(self):
        """Відсоток голосів"""
        total = self.vote.total_votes()
        if total == 0:
            return 0
        return round(self.vote_count() / total * 100, 1)


class UserVote(models.Model):
    """Голос користувача"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_votes',
        verbose_name="Користувач"
    )
    option = models.ForeignKey(
        VoteOption,
        on_delete=models.CASCADE,
        related_name='user_votes',
        verbose_name="Вибраний варіант"
    )
    voted_at = models.DateTimeField(auto_now=True, verbose_name="Дата голосування")

    class Meta:
        verbose_name = "Голос користувача"
        verbose_name_plural = "Голоси користувачів"
        # Один запис на пару (user, голосування) — унікальність через vote
        unique_together = []  # Унікальність контролюється через логіку view

    def __str__(self):
        return f"{self.user.username} → {self.option.text}"
