from django import forms
from django.contrib.auth.models import User
from .models import Profile, Project, Comment


def haveBlockHaracters(string: str):
    """Метод проверяющий на запретные символы в поле"""
    block_haracters = ['/', '|', '!', '<', '>', ' ', '"', "'", '@']
    for c in block_haracters:
        if c in string:
            return True
    return False


def isEmptyField(string: str):
    """Метод проверяющий поле на пустоту"""
    try:
        return not(bool(string.strip()))
    except:
        return True


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
        kwargs.setdefault("widget", MultipleFileInput(attrs={'accept': ".png,.jpg,.gif,.bmp,.jpeg"}))
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
        """Валидация всех полей проекта"""
        if (self.cleaned_data and isEmptyField(self.cleaned_data.get('name'))):
            raise forms.ValidationError("Нельзя создать проект с пустым названием")
        data = super().clean()
        current_name = data.get('name')
        names = [proj.name for proj in Project.objects.filter(autor=self.user)]
        if len(current_name) < 5:
            raise forms.ValidationError("Слишком короткое имя проекта!")
        if current_name in names:
            raise forms.ValidationError("Вы уже использовали данное имя проекта")
        if haveBlockHaracters(current_name):
            raise forms.ValidationError("В названии проекта нельзя использовать смиволы (/, |, <, >, !, ', \", ' ', @)")
        
       
        
    class Meta:
        model = Project
        fields = ('name', 'is_private', 'description', 'files')


class CommentForm(forms.ModelForm):
    def clean(self):
        # Проверяем текст комментария на то, является ли он пустым
        if isEmptyField(self.cleaned_data.get('text')):
            raise forms.ValidationError("Комментарий не может быть пустым")
        # Проверяем комментарий на спам (рандом буквы подряд)
        for string in self.cleaned_data.get('text').split():
            if len(string) > 20:
                raise forms.ValidationError("Просим вас не спамить! (Или не вводите слова длиннее 20 символов)")
        
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={"placeholder":"Введите текст комментария:"})
        }


class SearchUserForm(forms.ModelForm):
    def clean(request):
        # Заглушка так как без этого форма выбрасывает невалидность
        return

    class Meta:
        model = User
        fields = ('username',)
        widgets = {
                    'username': forms.TextInput(attrs={'autocomplete': 'off', 
                                                             'placeholder': 'Имя пользователя:'})
                }
        

class ProjectSearchForm(forms.ModelForm):
    def clean(request):
        # Заглушка так как без этого форма выбрасывает невалидность
        return
    
    class Meta:
        model = Project
        fields = ('name',)
        widgets = {
                    'name': forms.TextInput(attrs={'autocomplete': 'off', 
                                                             'placeholder': 'Название проекта:'})
                }


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
    def __init__(self, user, lastname, *args, **kwargs):
        self.user = user
        self.lastname = lastname
        super(ProjectEditForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        if (self.cleaned_data and isEmptyField(self.cleaned_data.get('name'))):
            raise forms.ValidationError("Нельзя создать проект с пустым названием")
        data = super().clean()
        current_name = data.get('name')
        names = [proj.name for proj in Project.objects.filter(autor=self.user)]
        if len(current_name) < 5:
            raise forms.ValidationError("Слишком короткое имя проекта!")
        if (current_name in names) and current_name != self.lastname:
            raise forms.ValidationError("Вы уже использовали данное имя проекта")
        if haveBlockHaracters(current_name):
            raise forms.ValidationError("В названии проекта нельзя использовать смиволы (/, |, <, >, !, ', \", ' ', @)")
    
    class Meta:
        model = Project
        fields = ('name', 'description', 'is_private',)


class ProjectFilterForm(forms.Form):
    """Форма фильтрации проектов на главной странице"""
    filters = (
        ('all', "Не выбрано"),
        ('name', "По алфавиту (а-я)"),
        ('-created_date', "Сначала новые"),
        ('created_date', "Сначала старые"),
        ('-likes', "По популярности")
    )
    filter = forms.ChoiceField(choices=filters)


class ConfirmProjectDelete(forms.Form):
    """Форма подтверждения удаления проекта"""
    projectname = forms.CharField()

    def __init__(self, right_name, *args, **kwargs):
        self.right_name = right_name
        super(ConfirmProjectDelete, self).__init__(*args, **kwargs)
    
    def clean(self):
        if self.cleaned_data['projectname'] != self.right_name:
            raise forms.ValidationError("Введенный текст не совпадает с именем проекта!")