from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off', 
                                                             'placeholder': ' ',
                                                             'readonly': True,
                                                             'onfocus': "this.removeAttribute('readonly')"}), max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off',
                                                                  'placeholder': ' ',
                                                                  'readonly': True,
                                                                  'onfocus': "this.removeAttribute('readonly')"}), max_length=30)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off',
                                                                  'placeholder': ' ',
                                                                  'readonly': True,
                                                                  'onfocus': "this.removeAttribute('readonly')"}), max_length=30)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2'] # те значения которые находятся в models.py
        labels = {'username': "Логин",
                  'password1': "Пароль",
                  'password2': "Повторите пароль"}

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')

