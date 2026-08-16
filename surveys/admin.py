from django.contrib import admin

from .models import Answer, Choice, Question, Survey, SurveyPage, SurveyResult


class SurveyPageInline(admin.TabularInline):
    model = SurveyPage
    extra = 1
    fields = ('order', 'title')
    show_change_link = True


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'pages_count', 'questions_count', 'created_by', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SurveyPageInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'is_required', 'order')
    show_change_link = True


@admin.register(SurveyPage)
class SurveyPageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'survey', 'order')
    list_filter = ('survey',)
    inlines = [QuestionInline]


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    fields = ('text', 'order')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'page', 'question_type', 'is_required', 'order')
    list_filter = ('page__survey', 'question_type', 'is_required')
    search_fields = ('text',)
    inlines = [ChoiceInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    can_delete = False
    readonly_fields = ('question', 'text_answer', 'choices')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SurveyResult)
class SurveyResultAdmin(admin.ModelAdmin):
    list_display = ('survey', 'user', 'passed_at')
    list_filter = ('survey',)
    search_fields = ('user__username',)
    readonly_fields = ('survey', 'user', 'passed_at')
    inlines = [AnswerInline]

    def has_add_permission(self, request):
        return False
