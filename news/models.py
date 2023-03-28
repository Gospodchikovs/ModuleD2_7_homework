from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # обновление рейтинга автора
    def update_rating(self) -> int:
        # Рейтинг состоит из следующих слагаемых:
        # - суммарный рейтинг статей автора умножается на 3;
        # - суммарный рейтинг все.х комментариев автора;
        # - суммарный рейтинг всех комментариев к статьям автора.
        post_sum = Post.objects.filter(author=self.id).aggregate(sum=Sum('rating'))['sum']
        user_sum = Comment.objects.filter(user=self.user).aggregate(sum=Sum('rating'))['sum']
        comment_sum = Comment.objects.filter(post__author=self).aggregate(sum=Sum('rating'))['sum']
        self.rating = post_sum * 3 + user_sum + comment_sum
        self.save() 
        return self.rating

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    topic = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscriber', verbose_name=u'Подписчик')

    def __str__(self):
        return f'{self.topic}'


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    TYPES = [(article, 'Статья'), (news, 'Новость')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=u'Автор')
    type = models.CharField(max_length=2, choices=TYPES, default=news, verbose_name=u'Тип')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name=u'Категория')
    heading = models.CharField(verbose_name=u'Заголовок', max_length=255)
    body = models.TextField(verbose_name=u'Текст')
    rating = models.IntegerField(default=0)

    # увеличенрие рейтинга на 1
    def like(self):
        self.rating += 1
        self.save()

    # уменьшение рейгинга на 1
    def dislike(self):
        self.rating -= 1           # рейтинг может быть отрицательным
        self.save()

    # получение превью стстьи с окончанием на '...'
    def preview(self) -> str:
        result = self.body[:124] + '...'
        return result

    # получение укороченного заголовка
    def shot_heading(self) -> str:
        result = self.heading[:50] + '...'
        return result

    def __str__(self):
        user = self.author.user.username
        return f'{user}: {self.heading[:30]} - {self.time_create}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу со стаьей
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    # увеличенрие рейтинга на 1
    def like(self):
        self.rating += 1            # рейтинг может быть отрицательным
        self.save()

    # уменьшение рейгинга на 1
    def dislike(self):
        self.rating -= 1            # рейтинг может быть отрицательным
        self.save()


class Subscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def add_subscriber(self, category, user):
        self.user = user
        self.category = category
        self.save()

    @staticmethod
    def delete_subscriber(category, user):
        Subscriber.objects.filter(user=user, category=category).delete()

    def __str__(self):
        user = self.user.username
        category = self.category.topic
        return f'{user}: {category[:30]}'
