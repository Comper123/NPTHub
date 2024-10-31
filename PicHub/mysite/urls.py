from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('account/', include('django.contrib.auth.urls')),
    path('register/', views.register, name="register"),
    # ! Сделать ссылку на профиль исходя из никнейма / id
    path('account/login', views.account_redirect, name='account_redirect'),
    path('profile/<str:name>', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="editprofile")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
