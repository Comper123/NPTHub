# Generated by Django 5.0 on 2024-11-03 20:23

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0007_profile_followers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарии')),
                ('data', models.DateField(default=django.utils.timezone.localdate)),
                ('autor', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'лайк',
                'verbose_name_plural': 'Лайки',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Проект', max_length=100, verbose_name='Название проекта')),
                ('is_public', models.BooleanField(default=True, verbose_name='Публичность')),
                ('is_pinned', models.BooleanField(default=False, verbose_name='Закрепленный')),
                ('created_date', models.DateField(default=django.utils.timezone.localdate)),
                ('description', models.TextField(default=None, verbose_name='Описание проекта')),
                ('autor', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='projects', to=settings.AUTH_USER_MODEL)),
                ('collaborators', models.ManyToManyField(related_name='collaborators', to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(related_name='projects', to='mysite.comment')),
                ('likes', models.ManyToManyField(related_name='projects', to='mysite.like')),
            ],
            options={
                'verbose_name': 'проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
    ]