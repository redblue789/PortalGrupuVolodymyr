from django.contrib import admin
from .models import Vote, VoteOption, UserVote


class VoteOptionInline(admin.TabularInline):
    model = VoteOption
    extra = 2
    fields = ['text', 'order']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'total_votes', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    inlines = [VoteOptionInline]
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(VoteOption)
class VoteOptionAdmin(admin.ModelAdmin):
    list_display = ['vote', 'text', 'order', 'vote_count']
    list_filter = ['vote']
    search_fields = ['text', 'vote__title']


@admin.register(UserVote)
class UserVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'option', 'voted_at']
    list_filter = ['voted_at']
    search_fields = ['user__username', 'option__text']
    readonly_fields = ['voted_at']
