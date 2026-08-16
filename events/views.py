import calendar as pycalendar
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm
from .models import Event

UKR_MONTHS = [
    '', 'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
    'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень',
]
UKR_DOW = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']


def can_manage_events(user):
    """Адміністратори (is_staff/superuser) та учасники групи Moderators."""
    return user.is_authenticated and (
        user.is_staff or user.groups.filter(name='Moderators').exists()
    )


def manage_required(view_func):
    """Пропускає далі лише тих, хто може керувати подіями."""
    def wrapped(request, *args, **kwargs):
        if not can_manage_events(request.user):
            messages.error(
                request,
                'Додавати, редагувати чи видаляти події можуть лише '
                'адміністратори та модератори.',
            )
            return redirect('events:feed')
        return view_func(request, *args, **kwargs)
    return wrapped


def feed_view(request):
    events = Event.objects.all()
    category = request.GET.get('category', '')
    query = request.GET.get('q', '').strip()
    if category:
        events = events.filter(category=category)
    if query:
        events = events.filter(title__icontains=query) | events.filter(location__icontains=query)
    context = {
        'events': events.order_by('date', 'time'),
        'categories': Event.Category.choices,
        'active_category': category,
        'query': query,
        'can_manage': can_manage_events(request.user),
        'today': date.today(),
    }
    return render(request, 'events/feed.html', context)


def calendar_view(request):
    today = date.today()
    year  = int(request.GET.get('year',  today.year))
    month = int(request.GET.get('month', today.month))
    if month < 1:
        month = 12; year -= 1
    elif month > 12:
        month = 1;  year += 1

    cal = pycalendar.Calendar(firstweekday=0)
    month_days = cal.itermonthdates(year, month)
    month_events = Event.objects.filter(date__year=year, date__month=month)
    events_by_day = {}
    for event in month_events:
        events_by_day.setdefault(event.date, []).append(event)

    weeks, week = [], []
    for day in month_days:
        week.append({
            'date': day, 'day': day.day,
            'in_month': day.month == month,
            'is_today': day == today,
            'events': events_by_day.get(day, []),
        })
        if len(week) == 7:
            weeks.append(week); week = []

    selected_day, selected_events = request.GET.get('day'), []
    if selected_day:
        try:
            y, m, d = (int(p) for p in selected_day.split('-'))
            selected_events = list(Event.objects.filter(date=date(y, m, d)))
        except (ValueError, TypeError):
            selected_day = None

    prev_month = month - 1 or 12
    prev_year  = year - 1 if month == 1  else year
    next_month = month + 1 if month < 12 else 1
    next_year  = year + 1 if month == 12 else year

    context = {
        'weeks': weeks, 'dow_labels': UKR_DOW,
        'month_label': f'{UKR_MONTHS[month]} {year}',
        'year': year, 'month': month,
        'prev_year': prev_year, 'prev_month': prev_month,
        'next_year': next_year, 'next_month': next_month,
        'today': today,
        'selected_day': selected_day, 'selected_events': selected_events,
        'can_manage': can_manage_events(request.user),
    }
    return render(request, 'events/calendar.html', context)


@login_required
@manage_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, f'Подію «{event.title}» додано.')
            return redirect('events:feed')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'is_edit': False})


@login_required
@manage_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Зміни до «{event.title}» збережено.')
            return redirect('events:feed')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'is_edit': True, 'event': event})


@login_required
@manage_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Подію «{title}» видалено.')
        return redirect('events:feed')
    return render(request, 'events/event_confirm_delete.html', {'event': event})
