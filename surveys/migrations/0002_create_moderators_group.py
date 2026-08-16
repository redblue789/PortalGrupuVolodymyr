from django.db import migrations

GROUP_NAME = 'Модератори'
MODEL_NAMES = ['survey', 'surveypage', 'question', 'choice']


def create_moderators_group(apps, schema_editor):
    # Дозволи (Permission) для щойно створених моделей звичайно генеруються
    # сигналом post_migrate ПІСЛЯ виконання всіх міграцій. Оскільки нам
    # потрібні вони прямо зараз (в межах цього ж запуску migrate), створюємо
    # їх примусово для поточного стану моделей.
    from django.apps import apps as global_apps
    from django.contrib.auth.management import create_permissions

    app_config = global_apps.get_app_config('surveys')
    app_config.models_module = True
    create_permissions(app_config, apps=apps, verbosity=0)

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    group, _ = Group.objects.get_or_create(name=GROUP_NAME)

    content_types = ContentType.objects.filter(app_label='surveys', model__in=MODEL_NAMES)
    permissions = Permission.objects.filter(content_type__in=content_types)
    group.permissions.set(permissions)

    view_content_types = ContentType.objects.filter(
        app_label='surveys', model__in=['surveyresult', 'answer']
    )
    view_permissions = Permission.objects.filter(
        content_type__in=view_content_types, codename__startswith='view_'
    )
    group.permissions.add(*view_permissions)


def remove_moderators_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name=GROUP_NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_moderators_group, remove_moderators_group),
    ]
