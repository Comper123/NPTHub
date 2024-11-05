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
    path('edit_profile/<str:name>', views.edit_profile, name="editprofile"),
    #Ссылка для подписок
    path('follow/<str:username>/', views.follow, name='follow'),
    #Ссылка для отписок
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    #Ссылка на сраницу подписчиков
    path('followers/', views.followers, name='followers'),
    #Ссылка на страницу создания проека
    path('create_project/', views.create_project, name='create_project')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
