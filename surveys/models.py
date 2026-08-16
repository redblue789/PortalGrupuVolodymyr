from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Survey(models.Model):
    """Опитування. Може складатись з кількох сторінок (SurveyPage)."""

    title = models.CharField('Назва', max_length=255)
    slug = models.SlugField('Слаг (для посилання)', max_length=255, unique=True, blank=True)
    description = models.TextField('Опис', blank=True)
    is_active = models.BooleanField(
        'Активне',
        default=True,
        help_text='Неактивні опитування не показуються користувачам у списку.',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_surveys',
    )
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'Опитування'
        verbose_name_plural = 'Опитування'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=False) or 'survey'
            slug = base_slug
            counter = 1
            while Survey.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f'{base_slug}-{counter}'
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('surveys:detail', kwargs={'slug': self.slug})

    @property
    def pages_count(self):
        return self.pages.count()

    @property
    def questions_count(self):
        return Question.objects.filter(page__survey=self).count()

    def has_content(self):
        return self.pages.exists() and self.questions_count > 0


class SurveyPage(models.Model):
    """Один етап (сторінка) багатоетапного опитування."""

    survey = models.ForeignKey(Survey, verbose_name='Опитування', related_name='pages', on_delete=models.CASCADE)
    title = models.CharField('Заголовок сторінки', max_length=255, blank=True)
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Сторінка опитування'
        verbose_name_plural = 'Сторінки опитування'
        ordering = ['order', 'id']
        unique_together = ('survey', 'order')

    def __str__(self):
        return self.title or f'Сторінка {self.order} ({self.survey.title})'


class Question(models.Model):
    TEXT = 'text'
    SINGLE = 'single'
    MULTIPLE = 'multiple'
    QUESTION_TYPES = [
        (TEXT, 'Текстова відповідь'),
        (SINGLE, 'Один варіант відповіді'),
        (MULTIPLE, 'Декілька варіантів відповіді'),
    ]

    page = models.ForeignKey(SurveyPage, verbose_name='Сторінка', related_name='questions', on_delete=models.CASCADE)
    text = models.CharField('Текст питання', max_length=500)
    question_type = models.CharField(
        'Тип питання', max_length=10, choices=QUESTION_TYPES, default=SINGLE
    )
    is_required = models.BooleanField('Обов\u2019язкове', default=True)
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text

    @property
    def survey(self):
        return self.page.survey

    @property
    def field_name(self):
        return f'question_{self.pk}'


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name='Питання', related_name='choices', on_delete=models.CASCADE)
    text = models.CharField('Варіант відповіді', max_length=255)
    order = models.PositiveIntegerField('Порядок', default=1)

    class Meta:
        verbose_name = 'Варіант відповіді'
        verbose_name_plural = 'Варіанти відповіді'
        ordering = ['order', 'id']

    def __str__(self):
        return self.text


class SurveyResult(models.Model):
    """Проходження опитування конкретним користувачем.

    Кожен користувач може мати лише один SurveyResult на опитування —
    при повторному проходженні старі відповіді видаляються і зберігаються нові.
    """

    survey = models.ForeignKey(Survey, verbose_name='Опитування', related_name='results', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Користувач',
        related_name='survey_results',
        on_delete=models.CASCADE,
    )
    passed_at = models.DateTimeField('Дата проходження', auto_now=True)

    class Meta:
        verbose_name = 'Результат проходження'
        verbose_name_plural = 'Результати проходження'
        unique_together = ('survey', 'user')
        ordering = ['-passed_at']

    def __str__(self):
        return f'{self.user} — {self.survey}'


class Answer(models.Model):
    result = models.ForeignKey(SurveyResult, verbose_name='Проходження', related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name='Питання', related_name='answers', on_delete=models.CASCADE)
    text_answer = models.TextField('Текстова відповідь', blank=True)
    choices = models.ManyToManyField(Choice, verbose_name='Обрані варіанти', blank=True, related_name='answers')

    class Meta:
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді'

    def __str__(self):
        return f'{self.question} — {self.result.user}'
