from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import RegistrationForm, ProfileForm
from .models import Profile


# Главная страница
def index(request):
    data = {
        
    }
    return render(request, "index.html", data)


# Изменяем ссылку на профиль после авторизации
@login_required
def account_redirect(request):
    return redirect('profile', name=request.user.username)


# Преобразуем представление базового шаблона авторизации и задаем ему новый redirect
# class MyLoginView():
#     def get_success_url(self):
#         url = self.get_redirect_url()
#         return url or reverse_lazy('/profile/', kwargs={'name': self.request.user.username})


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
            return redirect(f'/profile/{username}')
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {'registration_form': form})


# Страница изменения информации о пользователе
@login_required
@transaction.atomic
def edit_profile(request, name):
    # Проверяем пользователя на владение профилем
    if name == request.user.username:
        profile = Profile.objects.get(user=request.user.id)
        if request.method == "POST":
            profileform = ProfileForm(request.POST, request.FILES, instance=profile)
            if profileform.is_valid():
                profile.name = profileform.cleaned_data['name']
                profile.telegram = profileform.cleaned_data['telegram']
                profile.organization = profileform.cleaned_data['organization']
                profile.photo = profileform.cleaned_data['photo']
                if profileform.cleaned_data['photo'] != 'img/usersphotos/default.png':
                    profile.photo = profileform.cleaned_data['photo']
                profile.save()
                return redirect("profile", name=request.user.username)
        else:
            profileform = ProfileForm(instance=profile)

        data = {
            'profileform': profileform,
        }
        return render(request, "edit_profile.html", data)
    else:
        return render(request, "error.html", {'error': "403 Ошибка доступа",
                                              'code': 403})


@login_required
def profile(request, name):
    if (request.user.username == name):
        prof = request.user
    else:
        prof = User.objects.get(username=name)
    data = {
        'user_profile': prof,
        'profile': Profile.objects.get(user=prof),
        'followers': prof.profile.followers.all()
    }
    return render(request, "profile.html", data)


# Подписаться
@login_required
def follow(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    profile.followers.add(request.user)
    return redirect('profile', name=username)


# Отписаться
@login_required
def unfollow(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    profile.followers.remove(request.user)
    return redirect('profile', name=username)


# Страница подписчиков
@login_required
def followers(request):
    profile = Profile.objects.get(user=request.user.id)
    followers = profile.followers.all()
    # Формируем список словарей с подписчиками и их статусами
    followers_list = []
    for follower in followers:
        # Определяем статус подписчика
        if profile.is_friend(follower):
            status = "Друзья"
        else:
            status = "Подписчик"
        # Добавляем словарь
        followers_list.append(
            {
                'follower': follower,
                'status': status
            }
        )
    print(followers_list)
    data = {
        'followers': followers_list,
        'user_profile': profile
    }
    return render(request, "followers.html", data)
    