from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

MODERATORS_GROUP_NAME = 'Модератори'


def is_moderator(user):
    """Адміністратор (is_staff/superuser) або учасник групи «Модератори»."""
    if not user.is_authenticated:
        return False
    return user.is_staff or user.groups.filter(name=MODERATORS_GROUP_NAME).exists()


class ModeratorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Дозволяє доступ лише адміністраторам та модераторам."""

    def test_func(self):
        return is_moderator(self.request.user)
