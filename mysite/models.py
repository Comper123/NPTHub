from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import localdate


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Profile(models.Model):
    """Класс профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", default=None, null=True)
    name = models.CharField("Имя", max_length=100, default="User", null=True, blank=True,)
    telegram = models.CharField("Телеграм", max_length=50, blank=True, null=True, default="")
    register_date = models.DateField(default=localdate)
    photo = models.ImageField("Фото профиля", null=True, blank=True, upload_to="usersphotos/", 
                              default='usersphotos/default.png')
                                    
    age = models.IntegerField("Возраст", default=18)
    organization = models.CharField("Организация", max_length=100,
                                     default="Самозанятый")
    followers = models.ManyToManyField(User, related_name='following')

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'Профили'
    
    def is_friend(self, other: User):
        other_followers = Profile.objects.get(user=other).followers.all()
        if other in self.followers.all() and self.user in other_followers:
            return True
        return False
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name=instance.username)


# class Comment(models.Model):
#     """Класс комментариев"""
#     autor = models.OneToOneField(User, on_delete=models.CASCADE, related_name="projects", default=None, null=True)
#     text = models.TextField("Комментарии")
#     data = models.DateField(default=localdate)
    
    
# class Project(models.Model):
#     """Класс проекта (репозитория)"""
#     autor = models.OneToOneField(User, on_delete=models.CASCADE, related_name="projects", default=None, null=True)
#     name = models.CharField("Название проекта", max_length=100, default="Проект")
#     is_public = models.BooleanField("Публичность", default=True)
#     is_pinned = models.BooleanField("Закрепленный", default=False)
#     created_date = models.DateField(default=localdate)
#     description = models.TextField("Описание проекта", default=None)
#     comments = models.ManyToManyField(Comment, on_delete=models.CASCADE, related_name='comments')

