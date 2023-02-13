from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def update_rating(self):
        # Он состоит из следующего:
        # - суммарный рейтинг каждой статьи автора умножается на 3;
        # - суммарный рейтинг всех комментариев автора;
        # - суммарный рейтинг всех комментариев к статьям автора.
        # rating = 1
        # 3 * author_rating[0]['rating'] + sum_of_author_comments + sum_of_comments_to_author_articles
        return


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

    # уменьшение рейгинга на 1
    def dislike(self):
        self.rating -= 1           # рейтинг может быть отрицательным

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
        self.rating += 1

    # уменьшение рейгинга на 1
    def dislike(self):
        self.rating -= 1           # рейтинг может быть отрицательным
