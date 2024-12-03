from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from math import ceil
from django.core.files.storage import FileSystemStorage

from .forms import (
    RegistrationForm, 
    ProfileForm,
    ProjectForm,
    CommentForm,
    SearchUserForm,
    ProjectSearchForm,
    ProjectEditForm,
    ProjectFilterForm,
    ConfirmProjectDeleteForm,
    ProjectAddFilesForm,
    AddAchievementsForm
)
from .models import (
    Profile, 
    Project, 
    UploadedFile,
    Comment,
    Notification,
    Achievement
)
from .settings import PROJECT_PAGINATOR_COUNT


# Главная страница
def index(request):
    data = {
        
    }
    return render(request, "index.html", data)


# Изменяем ссылку на профиль после авторизации
@login_required
def account_redirect(request):
    return redirect('profile', name=request.user.username)


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
        return redirect('/admin/')
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
        'projects': projects[::-1],
        'pin_projects': pin_pined,
    }
    return render(request, "profile.html", data)


# Подписаться
@login_required
def follow(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    profile.followers.add(request.user)
    # & Создаем уведомление если такого еще нет
    try:
        notification = Notification.objects.get(autor=request.user, type=2, obj_id=user.id) # type 0 соответсвует типу лайка проекта
    except:
        # Создаем уведомление
        notification = Notification.objects.create()
        notification.text = "подписался на вас"
        notification.type = 2
        notification.autor = request.user
        notification.obj_id = user.id
        notification.obj_title = ""
        notification.save()
        # Добавляем уведомление в профиль пользователя который нам нужен
        user.profile.notifications.add(notification)
        # Устанавливаем то, что пользователь не прочел уведомления
        user.profile.is_check_notification = False
        user.profile.save()
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
    
    
    if request.method == "POST":
        form = ProjectForm(request.user, request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data['name'].strip():
            project = form.save(commit=False)
            project.autor = request.user
            project.name = form.cleaned_data['name']
            project.is_private = form.cleaned_data['is_private']
            project.description = form.cleaned_data['description']
            project.save()
            project = Project.objects.get(id=project.id)
            # Сохраняем все изображения которые добавлены в форму
            files = request.FILES.getlist('files')
            # print(request.FILES)
            # fs = FileSystemStorage()
            # filename = fs.save(files.name, files)
            # file_url = fs.url(filename)
            # return JsonResponse({'file_url': file_url})

            for file in files:
                f = UploadedFile.objects.create(file=file)
                project.files.add(f)
            project.save()
            return redirect(f'/{request.user.username}')
        else:
            form = ProjectForm(request.user, request.POST, request.FILES)
    else:
        form = ProjectForm(request.user)

    # if is_ajax(request):
    #     list = []
    #     print(request.FILES.getlist('files'))
    #     for file in request.FILES.getlist('files'):
    #         f = UploadedFile.objects.create(image=file)
    #         f.save()
    #         list.append(f)

    #  return render(request, 'blocks/photo_upload_block.html', {'files': list})
    
    data = {
        'projectform': form,
    }
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
            return redirect(f'/{project.autor.username}/{projectname}')
    else:
        comment_form = CommentForm()

    data = {
        'project': project,
        'comment_form': comment_form,
        'count_likes': len(project.likes.all())
    }
    return render(request, "project/project.html", data)


# Понравившиеся
@login_required
def liked_projects(request):
    data = {
        'projects': request.user.liked_projects.all(),
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
# @login_required
# def unpin(request, autor, name):
#     autor_id = User.objects.get(username=autor)
#     proj = Project.objects.get(autor=autor_id.id, name=name)
#     proj.is_pinned = False
#     proj.save() 
#     return redirect(f'/{request.user.username}/{proj.name}/')


# Закрепление проекта
# @login_required
# def pin(request, autor, name):
#     autor_id = User.objects.get(username=autor)
#     proj = Project.objects.get(autor=autor_id.id, name=name)
#     proj.is_pinned = True
#     proj.save() 
#     return redirect(f'/{autor_id.username}/{proj.name}/')


# Лайк проекта
# @login_required
# def like(request, autor, name):
#     autor_id = User.objects.get(username=autor)
#     proj = Project.objects.get(autor=autor_id.id, name=name)
#     request.user.profile.liked_projects.add(proj)
#     return redirect(f'/{autor_id.username}/{proj.name}/')


# Удаление из лайков проекта
# @login_required
# def unlike(request, autor, name):
#     autor_id = User.objects.get(username=autor)
#     proj = Project.objects.get(autor=autor_id.id, name=name)
#     request.user.profile.liked_projects.remove(proj)
#     return redirect(f'/{autor_id.username}/{proj.name}/')


# ajax запросы
@login_required
def project_ajax(request):
    if request.method == "POST":
        if request.POST.get("action") == "unpin":
            autor_name = request.POST.get("autor_name")
            project_name = request.POST.get("project_name")
            autor_id = User.objects.get(username=autor_name)
            proj = Project.objects.get(autor=autor_id.id, name=project_name)
            proj.is_pinned = False
            proj.save() 
            return JsonResponse({'text': 'Закрепить'})
        elif request.POST.get("action") == "pin":
            autor_name = request.POST.get("autor_name")
            project_name = request.POST.get("project_name")
            autor_id = User.objects.get(username=autor_name)
            proj = Project.objects.get(autor=autor_id.id, name=project_name)
            proj.is_pinned = True
            proj.save() 
            return JsonResponse({'text': 'Открепить'})
        elif request.POST.get("action") == "like":
            autor_name = request.POST.get("autor_name")
            project_name = request.POST.get("project_name")
            autor_id = User.objects.get(username=autor_name)
            proj = Project.objects.get(autor=autor_id.id, name=project_name)
            proj.likes.add(request.user)

            # & Создаем уведомление если такого еще нет
            notification = Notification.objects.get_or_create(autor=request.user, type=0, obj_id=proj.id)[0] # type 0 соответсвует типу лайка проекта
            if not notification.text:
                # Создаем уведомление
                notification.text = "оценил ваш проект"
                notification.obj_title = proj.name
                notification.save()
                # Добавляем уведомление в профиль пользователя который нам нужен
                autor_id.profile.notifications.add(notification)
                # Устанавливаем то, что пользователь не прочел уведомления
                autor_id.profile.is_check_notification = False
                autor_id.profile.save()

            return JsonResponse({'text': 'Убрать из понравившихся',
                                 'count': len(proj.likes.all())})
        elif request.POST.get("action") == "unlike":
            autor_name = request.POST.get("autor_name")
            project_name = request.POST.get("project_name")
            autor_id = User.objects.get(username=autor_name)
            proj = Project.objects.get(autor=autor_id.id, name=project_name)
            proj.likes.remove(request.user)
            return JsonResponse({'text': 'Добавить в понравившиеся',
                                 'count': len(proj.likes.all())})
        elif request.POST.get("action") == "like_comment":
            comment = Comment.objects.get(id=int(request.POST.get("id")))
            comment.liked_users.add(request.user)

            # & Создаем уведомление если такого еще нет
            notification = Notification.objects.get_or_create(autor=request.user, type=1, obj_id=comment.id) # type 0 соответсвует типу лайка проекта
            if not notification:
                # Создаем уведомление
                notification.text = "оценил ваш комментарий"
                notification.obj_title = comment.text[:20] + "..."
                notification.save()
                # Добавляем уведомление в профиль пользователя который нам нужен
                comment.autor.profile.notifications.add(notification)
                # Устанавливаем то, что пользователь не прочел уведомления
                comment.autor.profile.is_check_notification = False
                comment.autor.profile.save()

            return JsonResponse({'text': f"{len(list(comment.liked_users.all()))}"})
        elif request.POST.get("action") == "unlike_comment":
            comment = Comment.objects.get(id=int(request.POST.get("id")))
            comment.liked_users.remove(request.user)
            return JsonResponse({'text': f"{len(list(comment.liked_users.all()))}"})
        

# Контроллер удаления комментариев
@login_required
def delete_review(request):
    if request.method == "POST":
        com_id = request.POST.get("id")
        proj_id = request.POST.get("proj")
        com = Comment.objects.get(id=com_id)
        proj = Project.objects.get(id=proj_id)
        # & Создаем уведомление если такого еще нет
        try:
            notification = Notification.objects.get(autor=request.user, type=3, obj_id=com.id) # type 0 соответсвует типу лайка проекта
        except:
            # Создаем уведомление
            notification = Notification.objects.create()
            if request.user == com.autor:
                notification.text = "вы удалили комментарий: " + com.text[:30] + "..."
            else:
                notification.text = "Ваш комментарий был удален администратором: " + com.text[:30] + "..."
            notification.type = 3
            notification.autor = request.user
            notification.obj_id = com.id
            notification.obj_title = ""
            notification.save()
            # Добавляем уведомление в профиль пользователя который нам нужен
            com.autor.profile.notifications.add(notification)
            # Устанавливаем то, что пользователь не прочел уведомления
            com.autor.profile.is_check_notification = False
            com.autor.profile.save()
        proj.comments.remove(com)
        com.delete()
        return JsonResponse({'text': "Комментарий удален"})


# Контроллер страницы поиска пользователей
@login_required
def search_users(request):
    searchform = SearchUserForm(request.POST)
    data = {
        'title': "",
        'search_form': searchform,
        'user_profile': Profile.objects.get(user=request.user.id),
    }
    if request.method == "POST":
        if searchform.is_valid():
            users_list = []
            name = str(searchform.cleaned_data['username']).lower()
            for user in User.objects.all():
                if name in user.username.lower():
                    # print(user.username)
                    profile = user.profile
                    if profile.is_friend(request.user):
                        status = "Друзья"
                    elif profile.is_follower(request.user):
                        status = "Подписчик"
                    else:
                        status = ""
                    users_list.append(
                        {
                            'follower': user,
                            'status': status
                        }
                    )
            data['followers'] = users_list
            if len(users_list) == 0:
                data['searchstatus'] = "Ничего не найдено"
            else:
                data['searchstatus'] = ""
            return render(request, "followers.html", data)
        else:
            data['searchstatus'] = "Некорректный запрос!"
        searchform = SearchUserForm(request.POST)
    
    return render(request, "followers.html", data)


# Контроллер главной страницы
# @login_required
# def main_page(request):
#     projects = Project.objects.filter(is_private=False)
#     project_search_form = ProjectSearchForm(request.POST)
#     filter_form = ProjectFilterForm(request.POST)

#     data = {
#         'projects': projects,
#         'search_form': project_search_form,
#         'filter_form': filter_form,
#         'main_title': "Все проекты PicHub"
#     }

#     # Осуществляем поиск
#     if request.method == "POST" and project_search_form.is_valid():
#         # ? name__contains для проверки содержания в поле подстроки где name - поле
#         projects = Project.objects.filter(is_private=False,
#                     name__contains=str(project_search_form.cleaned_data['name']).lower())
#         data['projects'] = projects
#         # project_search_form = ProjectSearchForm(request.POST)
#         # Оформляем вывод только ответов на запрос
#         data['search_form'] = ""
#         data['filter_form'] = ""
#         data['main_title'] = f"Результаты поиска проекта {project_search_form.cleaned_data['name']}"

    
#     # Осуществляем фильтрацию проектов по полю
#     if request.method == "POST" and filter_form.is_valid():
#         filt = filter_form.cleaned_data['filter']
#         if filt == "-likes":
#             # ? Фильтрация по количеству связей многие ко многим (кол-во лайков)
#             data['projects'] = projects.filter(is_private=False).annotate(likes_count=Count('likes')).order_by('-likes_count')
#         elif filt == "all":
#             data['projects'] = Project.objects.filter(is_private=False)
#         else:
#             data['projects'] = projects.filter(is_private=False).order_by(filt)
#         data['filter'] = [i for i in ProjectFilterForm.filters if i[0] == filt][0][1]
#         filter_form = ProjectFilterForm(request.POST)
#     return render(request, "main.html", data)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# Контроллер главной страницы с пагинацией
@login_required
def main_page(request):
    projects = Project.objects.filter(is_private=False).order_by('-created_date')
    lenght = len(projects)
    project_search_form = ProjectSearchForm(request.POST)
    filter_form = ProjectFilterForm(request.POST)
    # Количество прогрузок проектов
    projects_per_page = PROJECT_PAGINATOR_COUNT
    paginator = Paginator(projects, projects_per_page)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            return HttpResponse('')
        projects = paginator.page(paginator.num_pages)
    if is_ajax(request):
        return render(request, 'blocks/all_projects.html', {'projects': projects})
    
    data = {
        'projects': projects,
        'search_form': project_search_form,
        'filter_form': filter_form,
        'main_title': "Все проекты PicHub",
        'max_pages': ceil(lenght / projects_per_page)
    }

    # Осуществляем поиск
    if request.method == "POST" and project_search_form.is_valid():
        # ? name__contains для проверки содержания в поле подстроки где name - поле
        projects = Project.objects.filter(is_private=False,
                    name__contains=str(project_search_form.cleaned_data['name']).lower())
        data['projects'] = projects
        # project_search_form = ProjectSearchForm(request.POST)
        # Оформляем вывод только ответов на запрос
        data['search_form'] = ""
        data['filter_form'] = ""
        data['main_title'] = f"Результаты поиска проекта {project_search_form.cleaned_data['name']}"

    
    # Осуществляем фильтрацию проектов по полю
    # if request.method == "POST" and filter_form.is_valid():
    #     filt = filter_form.cleaned_data['filter']
    #     projects_res = []
    #     for i in range(paginator.num_pages):
    #         for obj in paginator.get_page(i).object_list():
    #             projects_res.append(obj)
    #     if filt == "-likes":
    #         # ? Фильтрация по количеству связей многие ко многим (кол-во лайков)
    #         data['projects'] = projects_res.filter(is_private=False).annotate(likes_count=Count('likes')).order_by('-likes_count')
    #     elif filt == "all":
    #         data['projects'] = projects_res
    #     else:
    #         data['projects'] = projects_res.filter(is_private=False).order_by(filt)
    #     data['filter'] = [i for i in ProjectFilterForm.filters if i[0] == filt][0][1]
    #     filter_form = ProjectFilterForm(request.POST)
    return render(request, "main.html", data)


@login_required
def project_settings_edit(request, autor, projectname):
    autor_proj = User.objects.get(username=autor)
    project = Project.objects.get(autor=autor_proj.id, name=projectname)
    
    if request.method == "POST":
        edit_proj = ProjectEditForm(request.user, project.name, request.POST)
        if edit_proj.is_valid():
            project.name = edit_proj.cleaned_data['name']
            project.description = edit_proj.cleaned_data['description']
            project.is_private = edit_proj.cleaned_data['is_private']
            project.save()
            return redirect(f'/{autor_proj.username}/{project.name}/')
        else:
            edit_proj = ProjectEditForm(request.user, project.name, request.POST, instance=project)
    else:
        edit_proj = ProjectEditForm(request.user, project.name, instance=project)
    data = {
        'project': project,
        'projectform': edit_proj
    }
    return render(request, "project/project_settings_edit.html", data)


# Контроллер страница настроек (удаление проекта)
@login_required
def project_settings_delete(request, autor, projectname):
    autor_proj = User.objects.get(username=autor)
    project = Project.objects.get(autor=autor_proj.id, name=projectname)
    form = ConfirmProjectDeleteForm(project.name)
    if request.method == "POST":
        form = ConfirmProjectDeleteForm(project.name, request.POST)
        if form.is_valid():
            # Удаляем все объекты фотографий проекта
            for file in project.files.all():
                file.delete()
            # Удаляем проект
            project.delete()
            # Переносим пользователя на страницу его профиля
            return redirect(f"/{request.user.username}")
    
    data = {
        'project': project,
        'confirm_form': form,
    }
    return render(request, "project/project_settings_delete.html", data)


@login_required
def project_files(request, autor, projectname):
    autor_proj = User.objects.get(username=autor)
    project = Project.objects.get(autor=autor_proj.id, name=projectname)
    data = {
       'project': project,
    }
    return render(request, "project/project_files.html", data)


# Контроллер прочтения уведомлений
@login_required
def check_notifications(request):
    if request.method == "POST":
        request.user.profile.is_check_notification = True
        request.user.profile.save()
        for notif in request.user.profile.notifications.all():
            notif.is_check = True
            notif.save()
        return JsonResponse({'text': "Уведомления прочитаны"})


# Контроллер добавления фотографий в проект
@login_required
def project_settings_addfiles(request, autor, projectname):
    autor_proj = User.objects.get(username=autor)
    project = Project.objects.get(autor=autor_proj.id, name=projectname)
    if request.method == "POST":
        add_files_form = ProjectAddFilesForm(request.POST)
        if add_files_form.is_valid():
            files = request.FILES.getlist('files')
            for file in files:
                f = UploadedFile.objects.create(file=file)
                project.files.add(f)
            project.save()
        return redirect(f'/{project.autor.username}/{projectname}')

    else:
        add_files_form = ProjectAddFilesForm()

    data = {
        'project': project,
        'add_files_form': add_files_form
    }
    return render(request, "project/project_settings_addfiles.html", data)


# Контроллер добавления достижений
@login_required
def addachievements(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = AddAchievementsForm(request.POST)
        if form.is_valid():
            # Получаем фото достижений 
            # ! achievements так как в форме называется
            achievs = request.FILES.getlist('achievements')
            print(achievs)
            # Получаем профиль
            # Добавляем в цикле загруженные достижения
            for a in achievs:
                new_achiev = Achievement.objects.create(image=a)
                profile.achievements.add(new_achiev)
            # Сохраняем профиль пользователя с добавленными достижениями
            profile.save()
            return redirect(f'/{request.user.username}')
    else:
        form = AddAchievementsForm()
            
    data = {
        'add_achievements_form': form
    }
    return render(request, "add_achievements.html", data)


@login_required
def delete_file(request):
    if request.method == "POST":
        project = Project.objects.get(id=int(request.POST.get("proj")))
        # Проверяем на то сколько осталось файлов и юольше ли 1
        if len(project.files.all()) > 1:
            file = UploadedFile.objects.get(id=int(request.POST.get("id")))
            project.files.remove(file)
            file.delete()
            return JsonResponse({'result': True})
        else:
            return JsonResponse({'result': False})
