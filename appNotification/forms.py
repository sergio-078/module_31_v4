from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Response, News
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        label=_('Content *'),
        help_text=_('Use the editor to add images, videos, formatting and other rich content')
    )

    notify_subscribers = forms.BooleanField(
        required=False,
        initial=True,
        label=_('Notify category subscribers'),
        help_text=_('Send notifications to users subscribed to this category'),
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'checked': True
        })
    )

    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'image', 'video', 'notify_subscribers']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter post title'),
                'required': True
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
        }
        labels = {
            'category': _('Category *'),
            'title': _('Title *'),
            'content': _('Content *'),
            'image': _('Main Image'),
            'video': _('Main Video'),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError(_('Title must be at least 5 characters long'))
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content.strip()) < 20:
            raise forms.ValidationError(_('Content must be at least 20 characters long'))
        return content


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Write your response here...')
            }),
        }
        labels = {
            'text': _('Response text'),
        }

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 10:
            raise forms.ValidationError(_('Response must be at least 10 characters long'))
        return text


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'notify_subscribers']  # Добавляем поле
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter news title')
            }),
            'notify_subscribers': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'checked': True
            }),
        }
        labels = {
            'title': _('Title'),
            'content': _('Content'),
            'notify_subscribers': _('Notify subscribers about this news'),
        }

    content = forms.CharField(widget=CKEditorWidget(config_name='default'), label=_('Content'))

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError(_('Title must be at least 5 characters long'))
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 20:
            raise forms.ValidationError(_('Content must be at least 20 characters long'))
        return content
