# Generated by Django 5.0 on 2024-10-26 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_alter_profile_age_alter_profile_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='img/usersphotos/default.png', null=True, upload_to='img/usersphotos/', verbose_name='Фото профиля'),
        ),
    ]
