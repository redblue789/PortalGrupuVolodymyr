from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from SuperSchool.models import ForumThread, ForumPost
from events.models import Event
from datetime import date, time as dtime


USERS = [
    {
        "username": "admin",
        "password": "admin123",
        "email": "admin@school.ua",
        "first_name": "Адмін",
        "last_name": "Системи",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "moderator",
        "password": "mod123",
        "email": "mod@school.ua",
        "first_name": "Михайло",
        "last_name": "Модератор",
        "is_staff": True,
        "is_superuser": False,
    },
    {
        "username": "olena_k",
        "password": "olena123",
        "email": "olena@school.ua",
        "first_name": "Олена",
        "last_name": "Коваленко",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "dmytro_p",
        "password": "dmytro123",
        "email": "dmytro@school.ua",
        "first_name": "Дмитро",
        "last_name": "Петренко",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "sofia_m",
        "password": "sofia123",
        "email": "sofia@school.ua",
        "first_name": "Софія",
        "last_name": "Марченко",
        "is_staff": False,
        "is_superuser": False,
    },
]


class Command(BaseCommand):
    help = "Створює демо-користувачів, гілки та повідомлення для форуму"

    def handle(self, *args, **kwargs):
        created_users = {}

        # --- Create users ---
        for data in USERS:
            user, created = User.objects.get_or_create(username=data["username"])
            user.set_password(data["password"])
            user.email = data["email"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.is_staff = data["is_staff"]
            user.is_superuser = data["is_superuser"]
            user.save()
            created_users[data["username"]] = user
            status = "створено" if created else "оновлено"
            self.stdout.write(f"  Користувач '{data['username']}' — {status}")

        # --- Create demo threads & posts ---
        mod = created_users["moderator"]
        admin = created_users["admin"]
        olena = created_users["olena_k"]
        dmytro = created_users["dmytro_p"]
        sofia = created_users["sofia_m"]

        threads_data = [
            {
                "title": "Розклад занять на вересень",
                "created_by": mod,
                "posts": [
                    (mod, "Публікую оновлений розклад занять на вересень. Зверніть увагу на зміни у четвер."),
                    (olena, "Дякую! А коли буде розклад на жовтень?"),
                    (dmytro, "Чи будуть пари у суботу?"),
                    (mod, "Суботи поки що не плануються. Розклад на жовтень з'явиться в кінці вересня."),
                ],
            },
            {
                "title": "Оголошення: здача курсових робіт",
                "created_by": admin,
                "posts": [
                    (admin, "Нагадуємо, що дедлайн здачі курсових — 15 жовтня. Роботи надсилати на пошту кафедри."),
                    (sofia, "А можна здати раніше строку?"),
                    (admin, "Так, достроково приймаємо без обмежень."),
                    (olena, "Який формат файлу потрібен — PDF чи Word?"),
                    (admin, "PDF, будь ласка."),
                ],
            },
            {
                "title": "Питання до викладача з математики",
                "created_by": olena,
                "posts": [
                    (olena, "Чи буде консультація перед екзаменом з вищої математики?"),
                    (mod, "Консультація запланована на 10 грудня о 14:00 в ауд. 305."),
                    (dmytro, "Дякую за інформацію!"),
                    (sofia, "А чи можна записати консультацію на відео?"),
                ],
            },
            {
                "title": "Вільне спілкування групи",
                "created_by": mod,
                "posts": [
                    (mod, "Тут можна спілкуватись неформально — діліться новинами, жартами, корисними посиланнями!"),
                    (sofia, "Знайшла крутий сайт для підготовки до іспитів: quizlet.com — рекомендую!"),
                    (dmytro, "О, дякую! Я ним вже користуюсь)"),
                    (olena, "Хто йде на студентський концерт у п'ятницю? 🎵"),
                    (sofia, "Я точно іду!"),
                    (dmytro, "Теж планую)"),
                ],
            },
        ]

        for t_data in threads_data:
            thread, t_created = ForumThread.objects.get_or_create(
                title=t_data["title"],
                defaults={"created_by": t_data["created_by"]},
            )
            if t_created:
                self.stdout.write(f"  Гілка '{thread.title}' — створено")
                for author, content in t_data["posts"]:
                    ForumPost.objects.create(thread=thread, author=author, content=content)
            else:
                self.stdout.write(f"  Гілка '{thread.title}' — вже існує, пропускаємо")

        self.stdout.write(self.style.SUCCESS("\nГотово! Демо-дані успішно завантажені."))
        self.stdout.write("\nАкаунти для входу:")
        self.stdout.write("  admin       / admin123  (адміністратор)")
        self.stdout.write("  moderator   / mod123    (модератор)")
        self.stdout.write("  olena_k     / olena123  (студент)")
        self.stdout.write("  dmytro_p    / dmytro123 (студент)")
        self.stdout.write("  sofia_m     / sofia123  (студент)")

        # --- Create demo events ---
        events_data = [
            {
                "title": "Відкрита зустріч учасників групи",
                "description": "Обговорюємо плани на осінь та збираємо ідеї.",
                "date": date(2026, 8, 12), "time": dtime(18, 30),
                "location": "Спільнотний центр, вул. Шевченка 12",
                "category": Event.Category.MEETING, "status": Event.Status.PLANNED,
            },
            {
                "title": "Воркшоп з фасилітації дискусій",
                "description": "Практичне заняття для тих, хто веде зустрічі.",
                "date": date(2026, 8, 14), "time": dtime(16, 0),
                "location": "Онлайн, Zoom",
                "category": Event.Category.WORKSHOP, "status": Event.Status.PLANNED,
            },
            {
                "title": "Онлайн-звіт про діяльність за квартал",
                "description": "Підсумки роботи групи та відповіді на запитання.",
                "date": date(2026, 8, 17), "time": dtime(19, 0),
                "location": "Онлайн-трансляція",
                "category": Event.Category.ONLINE, "status": Event.Status.PLANNED,
            },
            {
                "title": "Осінній фестиваль спільноти",
                "description": "Щорічна подія з майстер-класами, музикою та ярмарком.",
                "date": date(2026, 8, 24), "time": dtime(12, 0),
                "location": "Парк культури, головна алея",
                "category": Event.Category.FESTIVAL, "status": Event.Status.PLANNED,
            },
            {
                "title": "Загальні збори координаторів",
                "description": "Розподіл обов'язків на наступний період.",
                "date": date(2026, 8, 5), "time": dtime(17, 0),
                "location": "Офіс групи, кімната 3",
                "category": Event.Category.BOARD, "status": Event.Status.DONE,
            },
        ]
        for ev_data in events_data:
            _, ev_created = Event.objects.get_or_create(
                title=ev_data["title"],
                defaults={k: v for k, v in ev_data.items() if k != "title"},
            )
            status = "створено" if ev_created else "вже існує"
            self.stdout.write(f"  Подія '{ev_data['title']}' — {status}")

        self.stdout.write(self.style.SUCCESS("\nВсе готово! 🎉"))
