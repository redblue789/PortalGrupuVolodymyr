from django import forms
from django.forms import inlineformset_factory
from .models import Vote, VoteOption


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву голосування'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Опис (необов\'язково)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'title': 'Назва голосування',
            'description': 'Опис',
            'is_active': 'Активне',
        }


class VoteOptionForm(forms.ModelForm):
    class Meta:
        model = VoteOption
        fields = ['text', 'order']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Варіант відповіді'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'width: 80px;'
            }),
        }
        labels = {
            'text': 'Текст варіанту',
            'order': 'Порядок',
        }


# Inline formset: варіанти всередині голосування
VoteOptionFormSet = inlineformset_factory(
    Vote,
    VoteOption,
    form=VoteOptionForm,
    extra=3,
    min_num=2,
    validate_min=True,
    can_delete=True,
)


class CastVoteForm(forms.Form):
    """Форма для участі у голосуванні"""
    option = forms.ModelChoiceField(
        queryset=VoteOption.objects.none(),
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Оберіть варіант',
        empty_label=None,
    )

    def __init__(self, vote, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['option'].queryset = vote.options.all()
