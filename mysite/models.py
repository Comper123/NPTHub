from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import localdate, now


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Achievement(models.Model):
    """Модель достижения"""
    image = models.ImageField(upload_to='userachievements/')
    uploaded_at = models.DateTimeField(default=now)
    
    class Meta:
        verbose_name = "достижение"
        verbose_name_plural = "Достижения"
        

class Notification(models.Model):
    """Модель уведомления"""
    TYPES = (
        (0, "like_project"),
        (1, "like_comment"),
        (2, "follow"),
        (3, "delete_comment")
    )
    text = models.CharField("Текст уведомления", max_length=200)
    type = models.CharField("Тип уведомления", choices=TYPES, max_length=30, default=0)
    date = models.DateTimeField("Время", default=now)
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    obj_id = models.IntegerField("id обьекта уведомления", null=False, default=0)
    obj_title = models.CharField("Имя обьекта уведомления", max_length=100, default="")
    is_check = models.BooleanField("Просмотрено", default=False)

    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'Уведомления'


class Comment(models.Model):
    """Модель комментария"""
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comments")
    text = models.TextField("Комментарии", max_length=2000)
    data = models.DateField(default=localdate)
    liked_users = models.ManyToManyField(User, blank=True)
    
    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'


class UploadedFile(models.Model):
    """Модель загружаемого файла"""
    file = models.ImageField(upload_to='usersprojects/')
    uploaded_at = models.DateTimeField(default=now)

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
    comments = models.ManyToManyField(Comment, related_name='project', blank=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators', blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_projects")
    files = models.ManyToManyField(UploadedFile, blank=True)
    # current_id = models.IntegerField("Основной файл", default=0)

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
    notifications = models.ManyToManyField(Notification)
    is_check_notification = models.BooleanField("Чтение комментариев", default=True)
    achievements = models.ManyToManyField(Achievement)
    
    # liked_projects = models.ManyToManyField(Project, related_name="likedprojects")

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

    def is_follower(self, other: User):
        if other in self.followers.all():
            return True
        return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name=instance.username)