from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # Ссылка на главную страницу
    path('', views.index, name="index"),
    # Использование встроенных ссылок авторизации
    path('account/', include('django.contrib.auth.urls')),
    #Ссылка на страницу проекта
    path('register/', views.register, name="register"),
    #Ссылка на сраницу авторизации
    path('account/login', views.account_redirect, name='account_redirect'),
    # Ссылка на страницу профиля пользователя
    path('<str:name>', views.profile, name="profile"),
    # Ссылка на странцу редактирования профиля
    path('edit_profile/', views.edit_profile, name="editprofile"),
    # Ссылка для подписок
    path('follow/<str:username>/', views.follow, name='follow'),
    #Ссылка для отписок
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    #Ссылка на сраницу подписчиков и друзей
    path('followers/', views.followers, name='followers'),
    # Ссылка на страницу создания проека
    path('create_project/', views.create_project, name='create_project'),
    # Ссылка загрузки фотографий при создании проекта
    # path('create_project/upload_images/', views.upload_image)
    
    # Ссылка на страницу понравившихся проектов
    path('liked_projects/' , views.liked_projects, name='liked_projects'),
    # Ссылка на страницу подписок пользователя
    path('follows/', views.follows, name='follows'),
    # Ссылка на страницу понравившихся проектов
    path('pined_projects/' , views.pined, name='pined'),
    # Ссылка на страницу настраивания проекта
    # path('<str:autor>/<str:projectname>/settings', views.create_project, name='project_settings'),
    # Ссылка для закрепления проекта
    # path('pinproj/<str:autor>/<str:name>/', views.pin, name="pin_proj"),
    # Ссылка для открепления проекта
    # path('unpinproj/<str:autor>/<str:name>/', views.unpin, name="unpin_proj"),
    # Ссылка лайк проекта
    # path('like_proj/<str:autor>/<str:name>/', views.like, name="like_proj"),
    # Ссылка дизлайк проекта
    # path('unlike_proj/<str:autor>/<str:name>/', views.unlike, name="unlike_proj"),
    # ajax на странице проекта
    path('project_ajax/', views.project_ajax),
    # Удаление комментария на странице проекта
    path('delete_review/', views.delete_review, name="delete_review"),
    # Ссылка на страницу проекта
    path('<str:autor>/<str:projectname>/', views.project, name='project'),
    # Ссылка на поиск пользователей
    path('search_users/', views.search_users, name="search_users"),
    # Ссылка на страницу со всеми проектами
    path('main/', views.main_page, name="main"),
    # Ссылка на страницу редактирования проекта
    path("<str:autor>/<str:projectname>/settings/edit/", views.project_settings_edit, name="settings_proj"),
    # Ссылка на страницу удаления проекта
    path("<str:autor>/<str:projectname>/settings/delete/", views.project_settings_delete, name="settings_proj_delete"),
    # Ссылка на страницу файлов проекта
    path('<str:autor>/<str:projectname>/files/',views.project_files, name="project_files"),
    # Обработка прочтения всех уведомлений пользователя
    path('check_notifications/', views.check_notifications),
    # Ссылка на страницу добавления файлов
    path("<str:autor>/<str:projectname>/settings/addfiles/", views.project_settings_addfiles, name="settings_proj_addfiles"),
    # Ссылка на добавление достижений
    path('addachievements/', views.addachievements, name="addachievements")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
