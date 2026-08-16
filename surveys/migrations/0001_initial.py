import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Слаг (для посилання)')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('is_active', models.BooleanField(default=True, help_text='Неактивні опитування не показуються користувачам у списку.', verbose_name='Активне')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_surveys', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Опитування',
                'verbose_name_plural': 'Опитування',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SurveyPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Заголовок сторінки')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Порядок')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='surveys.survey', verbose_name='Опитування')),
            ],
            options={
                'verbose_name': 'Сторінка опитування',
                'verbose_name_plural': 'Сторінки опитування',
                'ordering': ['order', 'id'],
                'unique_together': {('survey', 'order')},
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Текст питання')),
                ('question_type', models.CharField(choices=[('text', 'Текстова відповідь'), ('single', 'Один варіант відповіді'), ('multiple', 'Декілька варіантів відповіді')], default='single', max_length=10, verbose_name='Тип питання')),
                ('is_required', models.BooleanField(default=True, verbose_name='Обов\u2019язкове')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Порядок')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='surveys.surveypage', verbose_name='Сторінка')),
            ],
            options={
                'verbose_name': 'Питання',
                'verbose_name_plural': 'Питання',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Варіант відповіді')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Порядок')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='surveys.question', verbose_name='Питання')),
            ],
            options={
                'verbose_name': 'Варіант відповіді',
                'verbose_name_plural': 'Варіанти відповіді',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SurveyResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passed_at', models.DateTimeField(auto_now=True, verbose_name='Дата проходження')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='surveys.survey', verbose_name='Опитування')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_results', to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Результат проходження',
                'verbose_name_plural': 'Результати проходження',
                'ordering': ['-passed_at'],
                'unique_together': {('survey', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField(blank=True, verbose_name='Текстова відповідь')),
                ('choices', models.ManyToManyField(blank=True, related_name='answers', to='surveys.choice', verbose_name='Обрані варіанти')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='surveys.question', verbose_name='Питання')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='surveys.surveyresult', verbose_name='Проходження')),
            ],
            options={
                'verbose_name': 'Відповідь',
                'verbose_name_plural': 'Відповіді',
            },
        ),
    ]
