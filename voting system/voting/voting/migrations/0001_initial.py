from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Назва голосування')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активне')),
                ('created_by', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='created_votes',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Створив'
                )),
            ],
            options={
                'verbose_name': 'Голосування',
                'verbose_name_plural': 'Голосування',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VoteOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст варіанту')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('vote', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='options',
                    to='voting.vote',
                    verbose_name='Голосування'
                )),
            ],
            options={
                'verbose_name': 'Варіант відповіді',
                'verbose_name_plural': 'Варіанти відповіді',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_at', models.DateTimeField(auto_now=True, verbose_name='Дата голосування')),
                ('option', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='user_votes',
                    to='voting.voteoption',
                    verbose_name='Вибраний варіант'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='user_votes',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Користувач'
                )),
            ],
            options={
                'verbose_name': 'Голос користувача',
                'verbose_name_plural': 'Голоси користувачів',
            },
        ),
    ]
