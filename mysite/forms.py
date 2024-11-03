from django import forms
from django.contrib.auth.models import User
from .models import Profile, Project


class RegistrationForm(forms.ModelForm):
    """Форма регистрации"""
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off', 
                                                             'placeholder': ' ',
                                                             'readonly': True,
                                                             'onfocus': "this.removeAttribute('readonly')"}), max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off',
                                                                  'placeholder': ' ',
                                                                  'readonly': True,
                                                                  'onfocus': "this.removeAttribute('readonly')"}), max_length=30)
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off',
    #                                                               'placeholder': ' ',
    #                                                               'readonly': True,
    #                                                               'onfocus': "this.removeAttribute('readonly')"}), max_length=30)

    class Meta:
        model = User
        fields = ['username', 'password1'] # те значения которые находятся в models.py
    #     labels = {'username': "Логин",
    #               'password1': "Пароль",
    #               'password2': "Повторите пароль"}

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get('password1')
    #     password2 = cleaned_data.get('password2')
    #     if password1 != password2:
    #         raise forms.ValidationError('Пароли не совпадают')


class ProfileForm(forms.ModelForm):
    """Форма редактирования профиля"""
    class Meta:
        model = Profile
        fields = ('name', 'telegram', 'organization', 'photo')
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'Select_photo_div'})
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProjectForm(forms.ModelForm):
    """Форма создания проекта"""
    is_private = forms.BooleanField(required=False)
    files = MultipleFileField()
    class Meta:
        model = Project
        fields = ('name', 'is_private', 'description')