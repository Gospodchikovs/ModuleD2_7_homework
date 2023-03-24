from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Post, PostCategory, Subscriber, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime


@receiver(post_save, sender=PostCategory)
def postcategory_save_handler(sender, instance, created, **kwargs):
    if created:
        category = instance.category.id
        users = Subscriber.objects.filter(category=category).values('user__username', 'user__email').distinct()
        news = Post.objects.get(id=instance.post.id)
        for user in users:
            if (user['user__email'] != ''):
                news.username = user["user__username"]
                html_content = render_to_string('letter.html', {'news': news})
                msg = EmailMultiAlternatives(
                     subject=f'Новость для {user["user__username"]}',
                     body=news.body,
                     from_email='s.gospodchikov@yandex.ru',
                     to=[user['user__email']],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
    return


#
# проверка количества статейЮ открытых в течении суток
# поскольку тема дрмашней работы про сигналы - сделал через сигналы,
# но по моему эта логика должна быть где-то в моделях. Или я не прав?
#
@receiver(pre_save, sender=Post)
def post_presave_handler(sender, instance, **kwargs):
    control_date = datetime.datetime.now() - datetime.timedelta(days=1)                      # отматываем сутки назад
    posts = Post.objects.filter(author=instance.author.id, time_create__gt=control_date)     # список за последние сутки
    if len(posts) >= 3 and instance.pk is None:                     # проверяем, что речь идет о создании нового поста.
        raise Warning('Доступ запрещен. Запрещено создавать более трех статей за сутки!')
    return
