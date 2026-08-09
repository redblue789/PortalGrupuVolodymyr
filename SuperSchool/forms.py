from django import forms
from .models import ForumThread, ForumPost

class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 5:
            raise forms.ValidationError("Назва гілки повинна містити принаймні 5 символів.")
        return title

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 2:
            raise forms.ValidationError("Повідомлення не може бути порожнім або занадто коротким.")
        return content