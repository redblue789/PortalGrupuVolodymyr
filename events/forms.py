from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Наприклад: Відкрита зустріч учасників'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Коротко опишіть подію для учасників'
            }),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'location': forms.TextInput(attrs={
                'placeholder': 'Адреса або посилання на онлайн-зустріч'
            }),
        }
