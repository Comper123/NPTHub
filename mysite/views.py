from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import RegistrationForm


# Главная страница
def index(request):
    data = {
        
    }
    return render(request, "index.html", data)


# Страница регистрации
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['password1']
            user = User.objects.create_user(username, password=pwd)
            user.save()
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {'registration_form': form})