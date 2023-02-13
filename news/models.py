from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # обновление рейтинга
    def update_rating(self) -> int:
        # Рейтинг состоит из следующих слагаемых:
        # - рейтинг каждой статьи автора умножается на 3;
        # - суммарный рейтинг всех комментариев автора;
        # - суммарный рейтинг всех комментариев к статьям автора.
        result_rating = 0
        rating_list = Post.objects.filter(author=self.id).values('rating')
        for rating_object in rating_list:
            result_rating += rating_object.get('rating') * 3
        rating_list = Comment.objects.filter(user=self.user).values('rating')
        for rating in rating_list:
            result_rating += rating.get('rating')
        rating_list = Comment.objects.filter(post__author=self).values('rating')
        for rating in rating_list:
            result_rating += rating.get('rating')
        self.rating = result_rating
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
