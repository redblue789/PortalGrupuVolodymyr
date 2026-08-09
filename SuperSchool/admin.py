from django.contrib import admin
from .models import ForumThread, ForumPost

admin.site.register(ForumThread)
admin.site.register(ForumPost)