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
    # Ссылка на страницу проекта пользователя
    # path('<str:name>/<str:project>', views.project, name="project"),
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
    # Ссылка на страницу проекта
    path('<str:autor>/<str:projectname>/', views.project, name='project'),
    # Ссылка на страницу понравившихся проектов
    path('liked_projects/' , views.liked_projects, name='liked_projects')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
