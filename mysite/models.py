from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import localdate


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Comment(models.Model):
    """Модель комментария"""
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comments")
    text = models.TextField("Комментарии")
    data = models.DateField(default=localdate)
    liked_users = models.ManyToManyField(User)
    
    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    """Модель лайка проекта"""
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="likes")
    class Meta:
        verbose_name = 'лайк'
        verbose_name_plural = 'Лайки'


class UploadedFile(models.Model):
    """Модель загружаемого файла"""
    file = models.ImageField(upload_to='usersprojects/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"file_{self.id}"
    
    class Meta:
        verbose_name = 'файл'
        verbose_name_plural = 'Файлы'


class Project(models.Model):
    """Модель проекта (репозитория)"""
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="projects")
    name = models.CharField("Название проекта", max_length=100, blank=False)
    is_private = models.BooleanField("Приватный", default=False)
    is_pinned = models.BooleanField("Закрепленный", default=False)
    created_date = models.DateField(default=localdate)
    description = models.TextField("Описание проекта", blank=True)
    comments = models.ManyToManyField(Comment, related_name='projects', blank=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators', blank=True)
    likes = models.ManyToManyField(Like, related_name='projects', blank=True)
    files = models.ManyToManyField(UploadedFile)
    # Имя для пути к файлу
    # slug = models.SlugField(unique=True, default=slugify(name))
    
    # def save(self, *args, **kwargs):
    #     """Метод сохранения экземпляра"""
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)
    
    class Meta:
        # ! unique_together для того чтобы уникальность была для отдельного пользователя 
        # ! (у одного пользователя не может быть проектов с одинаковыми названиями)
        # unique_together = 'autor', 'slug'
        # ! Отображение в базе данных
        verbose_name = 'проект'
        verbose_name_plural = 'Проекты'


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", default=None, null=True)
    name = models.CharField("Имя", max_length=100, default="User", null=True, blank=True)
    telegram = models.CharField("Телеграм", max_length=50, blank=True, null=True, default="")
    register_date = models.DateField(default=localdate)
    photo = models.ImageField("Фото профиля", null=True, blank=True, upload_to="usersphotos/", 
                              default='usersphotos/default.png')
                                    
    age = models.IntegerField("Возраст", default=18)
    organization = models.CharField("Организация", max_length=100,
                                     default="Самозанятый")
    followers = models.ManyToManyField(User, related_name='following')
    liked_projects = models.ManyToManyField(Project, related_name="likedprojects")

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

