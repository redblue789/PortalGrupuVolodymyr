from django.conf import settings
from django.db import models
from django.urls import reverse


class Event(models.Model):

    class Category(models.TextChoices):
        MEETING = 'meeting', 'Зустріч'
        WORKSHOP = 'workshop', 'Воркшоп'
        ONLINE = 'online', 'Онлайн'
        FESTIVAL = 'festival', 'Фестиваль'
        BOARD = 'board', 'Збори'

    class Status(models.TextChoices):
        PLANNED = 'planned', 'Заплановано'
        DONE = 'done', 'Завершено'
        CANCELLED = 'cancelled', 'Скасовано'

    title = models.CharField('Назва', max_length=200)
    description = models.TextField('Опис', blank=True)
    date = models.DateField('Дата')
    time = models.TimeField('Час')
    location = models.CharField('Місце проведення', max_length=255, blank=True)
    category = models.CharField(
        'Категорія', max_length=20, choices=Category.choices, default=Category.MEETING
    )
    status = models.CharField(
        'Статус', max_length=20, choices=Status.choices, default=Status.PLANNED
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events_created',
    )
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        ordering = ['date', 'time']
        verbose_name = 'Подія'
        verbose_name_plural = 'Події'

    def __str__(self):
        return f'{self.title} — {self.date:%d.%m.%Y}'

    def get_absolute_url(self):
        return reverse('events:feed')
