# Generated by Django 4.1.6 on 2023-03-07 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_post_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
    ]
