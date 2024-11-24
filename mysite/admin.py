from django.contrib import admin
from mysite.models import (
    Profile, 
    Project, 
    UploadedFile,
    Comment,
    Notification
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo', 'organization']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['autor', 'created_date', 'name']


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['file', 'uploaded_at']


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['autor', 'text']


@admin.register(Notification)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['text', 'autor', 'type', 'date', 'is_check']