# Generated by Django 5.0 on 2024-11-05 13:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0018_alter_project_files'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploadedfile',
            options={'verbose_name': 'файл', 'verbose_name_plural': 'Файлы'},
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together={('autor', 'name')},
        ),
    ]
