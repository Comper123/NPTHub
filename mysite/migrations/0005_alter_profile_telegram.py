# Generated by Django 5.1.2 on 2024-11-01 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telegram',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Телеграм'),
        ),
    ]
