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
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Назва')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Час')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='Місце проведення')),
                ('category', models.CharField(choices=[('meeting', 'Зустріч'), ('workshop', 'Воркшоп'), ('online', 'Онлайн'), ('festival', 'Фестиваль'), ('board', 'Збори')], default='meeting', max_length=20, verbose_name='Категорія')),
                ('status', models.CharField(choices=[('planned', 'Заплановано'), ('done', 'Завершено'), ('cancelled', 'Скасовано')], default='planned', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Оновлено')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events_created', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Подія',
                'verbose_name_plural': 'Події',
                'ordering': ['date', 'time'],
            },
        ),
    ]
