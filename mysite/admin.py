from django.contrib import admin
from mysite.models import Profile, Project


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo', 'organization']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['autor', 'created_date', 'name']
