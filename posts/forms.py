from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': _('Текст поста'),
            'group': _('Группа')
        }
        help_texts = {
            'text': _('Напишите текст поста'),
            'group': _('Выберите группу')
        }
        error_messages = {
            'text': {
                'required': _("Это обязательное поле."),
            }

        }


    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Это поле обязательно для заполнения!')
        return data
