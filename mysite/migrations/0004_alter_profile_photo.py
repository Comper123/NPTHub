# Generated by Django 5.0 on 2024-10-26 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='usersphotos/default.png', null=True, upload_to='usersphotos/', verbose_name='Фото профиля'),
        ),
    ]