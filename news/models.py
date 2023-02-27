from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    rating = models.IntegerField()
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


class Category(models.Model):
    topic = models.CharField(max_length=255, unique=True)


article = 'AR'
news = 'NW'
TYPES = [(article, 'Статья'), (news, 'Новость')]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255)
    body = models.TextField()
    rating = models.IntegerField()

    # увеличенрие рейтинга на 1
    def like(self):
        self.rating += 1
        self.save()

    # уменьшение рейгинга на 1
    def dislike(self):
        self.rating -= 1           # рейтинг может быть отрицательным
        self.save()

    # получение превью строки с окончанием на '...'
    def preview(self) -> str:
        result = self.body[:124] + '...'
        return result

    def __str__(self):
        user = self.author.user.username
        return f'{user}: {self.heading[:30]}'


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
