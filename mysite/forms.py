from django import forms
from django.contrib.auth.models import User
from .models import Profile, Project, Comment


class RegistrationForm(forms.ModelForm):
    """Форма регистрации"""
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off', 
                                                             'placeholder': ' ',}), max_length=100)
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off',
                                                                  'placeholder': ' ',
                                                                  'data-toggle': 'password'}), max_length=30)
    class Meta:
        model = User
        fields = ['username', 'password1'] # те значения которые находятся в models.py

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('username') == 'admin':
            raise forms.ValidationError('Недостаточно прав')
        
        usernames = [user.username for user in User.objects.all()]
        if cleaned_data.get('username') in usernames:
            raise forms.ValidationError('Пользователь с таким именем уже существует')


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
    choices = (
        (0, ''), # Публичный
        (1, '') # Приватный
    )
    is_private = forms.TypedChoiceField(
                         choices=choices,
                         widget=forms.RadioSelect, 
                         coerce=int,  
                    )
    files = MultipleFileField()
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProjectForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        current_name = data.get('name')
        names = [proj.name for proj in Project.objects.filter(autor=self.user)]
        if current_name in names:
            raise forms.ValidationError("Вы уже использовали данное имя проекта")
        
    class Meta:
        model = Project
        fields = ('name', 'is_private', 'description', 'files')


class ProjectEditForm(forms.ModelForm):
    """Форма редактирования проекта"""
    choices = (
        (0, ''), # Публичный
        (1, '') # Приватный
    )
    is_private = forms.TypedChoiceField(
                         choices=choices,
                         widget=forms.RadioSelect, 
                         coerce=int,  
                    )
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProjectForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        data = super().clean()
        current_name = data.get('name')
        names = [proj.name for proj in Project.objects.filter(autor=self.user)]
        if current_name in names:
            raise forms.ValidationError("Вы уже использовали данное имя проекта")
        
    class Meta:
        model = Project
        fields = ('name', 'description', 'is_private')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea()
        }