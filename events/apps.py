from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def create_moderators_group(sender, **kwargs):
    """
    Після кожної міграції переконуємось, що існує група "Moderators"
    з правами додавати/редагувати/видаляти/переглядати події.
    Адміністратор потім лише додає користувача в цю групу через
    Users -> обраний користувач -> Groups в адмін-панелі.
    """
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from events.models import Event

    group_name = getattr(settings, 'MODERATORS_GROUP_NAME', 'Moderators')
    group, _ = Group.objects.get_or_create(name=group_name)

    content_type = ContentType.objects.get_for_model(Event)
    permissions = Permission.objects.filter(
        content_type=content_type,
        codename__in=['add_event', 'change_event', 'delete_event', 'view_event'],
    )
    group.permissions.set(permissions)


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
    verbose_name = 'Події'

    def ready(self):
        post_migrate.connect(create_moderators_group, sender=self)
