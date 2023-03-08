# Generated by Django 4.1.6 on 2023-03-07 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_post_author_alter_post_heading'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(choices=[('AR', 'Статья'), ('NW', 'Новость')], default='NW', max_length=2, verbose_name='Тип'),
        ),
    ]
