# Generated by Django 5.0 on 2024-11-23 23:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0047_alter_notification_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время'),
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]