from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    """Головна сторінка порталу."""
    return render(request, 'home/index.html')
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import ForumThread, ForumPost
from .forms import ForumThreadForm, ForumPostForm


def is_staff_or_moderator(user):
    """Return True if user is admin or has moderator status (staff flag)."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# ---------------------------------------------------------------------------
# Thread views
# ---------------------------------------------------------------------------

def thread_list(request):
    """Public view — lists all forum threads."""
    threads = ForumThread.objects.select_related('created_by').order_by('-created_at')
    return render(request, 'forum/thread_list.html', {'threads': threads})


def thread_detail(request, pk):
    """Public view — shows a thread and all its posts; lets authenticated users post."""
    thread = get_object_or_404(ForumThread, pk=pk)
    posts = thread.posts.select_related('author').order_by('created_at')
    form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ForumPostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.thread = thread
                post.author = request.user
                post.save()
                messages.success(request, 'Повідомлення додано.')
                return redirect('thread_detail', pk=pk)
        else:
            form = ForumPostForm()

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'posts': posts,
        'form': form,
    })


@login_required
def create_thread(request):
    """Only staff/moderators can create threads."""
    if not is_staff_or_moderator(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = ForumThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.save()
            messages.success(request, 'Гілку створено.')
            return redirect('thread_list')
    else:
        form = ForumThreadForm()

    return render(request, 'forum/thread_form.html', {
        'form': form,
        'action': 'Створити',
    })


@login_required
def edit_thread(request, pk):
    """Only staff/moderators can edit threads."""
    if not is_staff_or_moderator(request.user):
        raise PermissionDenied

    thread = get_object_or_404(ForumThread, pk=pk)

    if request.method == 'POST':
        form = ForumThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            messages.success(request, 'Гілку оновлено.')
            return redirect('thread_list')
    else:
        form = ForumThreadForm(instance=thread)

    return render(request, 'forum/thread_form.html', {
        'form': form,
        'action': 'Редагувати',
        'thread': thread,
    })


@login_required
def delete_thread(request, pk):
    """Only staff/moderators can delete threads."""
    if not is_staff_or_moderator(request.user):
        raise PermissionDenied

    thread = get_object_or_404(ForumThread, pk=pk)

    if request.method == 'POST':
        thread.delete()
        messages.success(request, 'Гілку видалено.')
        return redirect('thread_list')

    return render(request, 'forum/thread_confirm_delete.html', {'thread': thread})
