from django import forms

from .models import Question, Survey


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Назва опитування',
            'description': 'Опис',
            'is_active': 'Активне (показувати користувачам)',
        }


def build_page_form_class(page):
    """Динамічно створює клас Form з полем для кожного питання сторінки."""

    fields = {}
    for question in page.questions.all():
        field_kwargs = {
            'label': question.text,
            'required': question.is_required,
        }
        if question.question_type == Question.TEXT:
            field = forms.CharField(
                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                **field_kwargs,
            )
        else:
            choices = [(choice.pk, choice.text) for choice in question.choices.all()]
            if question.question_type == Question.SINGLE:
                field = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect,
                    **field_kwargs,
                )
            else:  # MULTIPLE
                field = forms.MultipleChoiceField(
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple,
                    **field_kwargs,
                )
        fields[question.field_name] = field

    return type('SurveyPageForm', (forms.Form,), fields)
