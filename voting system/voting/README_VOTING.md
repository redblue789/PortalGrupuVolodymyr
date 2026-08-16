# Система голосувань — інструкція інтеграції

## Файли які потрібно додати в проект

```
voting/
├── __init__.py
├── apps.py
├── admin.py
├── models.py
├── forms.py
├── views.py
├── urls.py
└── migrations/
    ├── __init__.py
    └── 0001_initial.py

templates/
└── voting/
    ├── vote_list.html
    ├── vote_detail.html
    ├── vote_form.html
    └── vote_confirm_delete.html
```

## Крок 1 — Скопіювати папку `voting/`
Скопіюй папку `voting/` поруч з `SuperSchool/` і `PortalGroup/`:
```
PortalGrupuVolodymyr-main/
├── PortalGroup/
├── SuperSchool/
├── voting/          ← сюди
├── db.sqlite3
└── manage.py
```

## Крок 2 — Скопіювати шаблони
Скопіюй папку `templates/voting/` у вже існуючу папку `templates/` проекту.

## Крок 3 — settings.py
Відкрий `PortalGroup/settings.py` і додай `'voting'` до `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... існуючі додатки ...
    'SuperSchool',
    'voting',   # ← додати
]
```

## Крок 4 — urls.py
Відкрий `PortalGroup/urls.py` і додай маршрут:

```python
from django.urls import path, include

urlpatterns = [
    # ... існуючі маршрути ...
    path('voting/', include('voting.urls')),  # ← додати
]
```

## Крок 5 — Міграції
```bash
python manage.py migrate
```

## Крок 6 — Перевірка
Запусти сервер і відкрий: http://127.0.0.1:8000/voting/

---

## Функціонал по ТЗ

| Вимога | Реалізовано |
|--------|------------|
| Всі зареєстровані користувачі можуть голосувати | ✅ `LoginRequiredMixin` |
| Користувач голосує лише раз, переголосування зберігає тільки останній | ✅ `CastVoteView` видаляє старий і створює новий |
| Адмін/модератор може створювати голосування | ✅ `VoteCreateView` з перевіркою `is_staff` |
| Адмін/модератор може редагувати | ✅ `VoteUpdateView` |
| Адмін/модератор може видаляти | ✅ `VoteDeleteView` |
| Всі користувачі бачать результати | ✅ результати видно на `vote_detail` без авторизації |

## Ролі (як у ТЗ)

- **Суперюзер / адміністратор** (`is_superuser=True`) — повний доступ
- **Модератор** (`is_staff=True`) — може створювати/редагувати/видаляти
- **Звичайний користувач** — може голосувати і переглядати результати
- **Анонімний** — лише перегляд результатів

> Якщо в проекті є своя кастомна система ролей — замініть перевірку
> `u.is_staff or u.is_superuser` в `AdminOrModeratorMixin` на свою логіку.

## Посилання у шаблонах

Якщо хочеш додати посилання на голосування з головної сторінки або навігації:
```html
<a href="{% url 'voting:vote_list' %}">Голосування</a>
```
