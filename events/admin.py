from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display   = ('title', 'date', 'time', 'category', 'status', 'location', 'created_by')
    list_filter    = ('category', 'status', 'date')
    search_fields  = ('title', 'description', 'location')
    date_hierarchy = 'date'
    ordering       = ('date', 'time')

    fieldsets = (
        (None,         {'fields': ('title', 'description')}),
        ('Коли й де',  {'fields': ('date', 'time', 'location')}),
        ('Класифікація',{'fields': ('category', 'status')}),
        ('Службова',   {'fields': ('created_by',)}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
