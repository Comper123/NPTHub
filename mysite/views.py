from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.http import JsonResponse


from .forms import (
    RegistrationForm, 
    ProfileForm,
    ProjectForm,
    CommentForm,
)
from .models import (
    Profile, 
    Project, 
    UploadedFile,
    Comment
)


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
            return redirect(f'/{username}')
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {'registration_form': form})


# Страница изменения информации о пользователе
@login_required
@transaction.atomic
def edit_profile(request):
    # Проверяем пользователя на владение профилем
    # if name == request.user.username:
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
    # else:
        # return render(request, "error.html", {'error': "403 Ошибка доступа",
                                            #   'code': 403})


@login_required
def profile(request, name):
    if (name == 'admin' and request.user.is_superuser):
        return redirect('admin/')
    if (request.user.username == name):
        # Если профиль текущего пользователя
        prof = request.user
        pin_pined = Project.objects.filter(autor=prof, is_pinned=True)
        projects = Project.objects.filter(autor=prof, is_pinned=False)
    else:
        # Профиль другого пользователя
        prof = User.objects.get(username=name)
        pin_pined = Project.objects.filter(autor=prof, is_pinned=True, is_private=False)
        projects = Project.objects.filter(autor=prof, is_pinned=False, is_private=False)
    data = {
        'user_profile': prof,
        'profile': Profile.objects.get(user=prof),
        'followers': prof.profile.followers.all(),
        'projects': projects,
        'pin_projects': pin_pined,
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
    data = {
        'followers': followers_list,
        'user_profile': profile,
        'title': "Ваши подписчики и друзья:"
    }
    return render(request, "followers.html", data)


# Страница создания проекта
@login_required
def create_project(request):
    data = {}
    if request.method == "POST":
        form = ProjectForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.autor = request.user
            project.name = form.cleaned_data['name']
            project.is_private = form.cleaned_data['is_private']
            project.description = form.cleaned_data['description']
            project.save()
            project = Project.objects.get(id=project.id)
            # Сохраняем все изображения которые добавлены в форму
            files = request.FILES.getlist('files')
            # print(files)
            # print(request.FILES.getlist('files'))
            # print(request.FILES)

            for file in files:
                f = UploadedFile.objects.create(file=file)
                project.files.add(f)
            return redirect(f'/{request.user.username}')
        else:
            form = ProjectForm(request.user, request.POST, request.FILES)
    else:
        form = ProjectForm(request.user)

    data['projectform'] = form
    return render(request, "project/create_project.html", data)


# @login_required
# def upload_image(request):
#     proj = Project.objects.get(autor=autor, name=project)
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#         f = UploadedFile.objects.create(file=file)
#         proj.files.add(f)


# Проект
@login_required
def project(request, autor, projectname):
    autor_proj = User.objects.get(username=autor)
    project = Project.objects.get(autor=autor_proj.id, name=projectname)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            # comment = Comment.objects.create(autor=request.user)
            comment.autor = request.user
            comment.text = comment_form.cleaned_data['text']
            comment.save()
            # Добавляем комментарий в комментарии проекта
            project.comments.add(comment)
            return redirect(f'/{request.user.username}/{projectname}')

    else:
        comment_form = CommentForm()

    data = {
        'project': project,
        'comment_form': comment_form,
    }
    return render(request, "project/project.html", data)


# Понравившиеся
@login_required
def liked_projects(request):
    data = {
        'projects': request.user.profile.liked_projects.all(),
        'type': "Понравившиеся вам проекты:",
        'status': "понравившихся"
    }
    return render(request, 'like_project.html', data)


# Страница избранных проектов текущего пользователя
@login_required
def pined(request):
    data = {
        'projects': Project.objects.filter(autor=request.user.id,
                                           is_pinned=True),
        'type': "Ваши избранные проекты:",
        'status': "избранных"
    }
    return render(request, 'like_project.html', data)


# Страница подписок пользователя
@login_required
def follows(request):
    profiles = Profile.objects.all()
    # Формируем список словарей с подписками и их статусами
    follows_list = []
    for p in profiles:
        if request.user in p.followers.all():
            user = User.objects.get(profile=p)
            if user not in request.user.profile.followers.all():
                follows_list.append(
                    {
                        'follower': user,
                        'status': "Подписки"
                    }
                )
    data = {
        'followers': follows_list,
        'title': "Ваши подписки:"
    }
    return render(request, "followers.html", data)


# Открепление проекта
@login_required
def unpin(request, autor, name):
    autor_id = User.objects.get(username=autor)
    proj = Project.objects.get(autor=autor_id.id, name=name)
    proj.is_pinned = False
    proj.save() 
    return redirect(f'/{request.user.username}/{proj.name}/')


# Закрепление проекта
@login_required
def pin(request, autor, name):
    autor_id = User.objects.get(username=autor)
    proj = Project.objects.get(autor=autor_id.id, name=name)
    proj.is_pinned = True
    proj.save() 
    return redirect(f'/{autor_id.username}/{proj.name}/')


# Лайк проекта
@login_required
def like(request, autor, name):
    autor_id = User.objects.get(username=autor)
    proj = Project.objects.get(autor=autor_id.id, name=name)
    request.user.profile.liked_projects.add(proj)
    return redirect(f'/{autor_id.username}/{proj.name}/')


# Удаление из лайков проекта
@login_required
def unlike(request, autor, name):
    autor_id = User.objects.get(username=autor)
    proj = Project.objects.get(autor=autor_id.id, name=name)
    request.user.profile.liked_projects.remove(proj)
    return redirect(f'/{autor_id.username}/{proj.name}/')


# ajax запросы
def project_ajax(request):
    if request.method == "POST":
        autor_name = request.POST.get("autor_name")
        project_name = request.POST.get("project_name")
        autor_id = User.objects.get(username=autor_name)
        if request.POST.get("action") == "unpin":
            proj = Project.objects.get(autor=autor_id.id, name=project_name)
            proj.is_pinned = False
            proj.save() 
            return JsonResponse({'text': 'Закрепить'})
        elif request.POST.get("action") == "pin":
            proj = Project.objects.get(autor=autor_id.id, name=project_name)
            proj.is_pinned = True
            proj.save() 
            return JsonResponse({'text': 'Открепить'})