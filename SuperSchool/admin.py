from django.contrib import admin
from .models import Student, Subject, Grade


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'grade_level', 'description')
    search_fields = ('last_name', 'first_name', 'grade_level')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    # Прибрали 'comment', оскільки його немає в моделі Grade
    list_display = ('student', 'subject', 'score', 'date_added')
    list_filter = ('subject', 'student__grade_level', 'date_added')
    search_fields = ('student__last_name', 'student__first_name', 'subject__name')
    list_editable = ('score',)