from news.models import Category, PostCategory, Post, Author, Comment
from django.contrib.auth.models import User

user1 = User.objects.create_user(username='user1', email='user1@e.mail', password='user1_password')
user2 = User.objects.create_user(username='user2', email='user2@e.mail', password='user2_password')

author1 = Author.objects.create(user=user1, rating=0)
author2 = Author.objects.create(user=user2, rating=0)

category1 = Category.objects.create(topic='Sport')
category2 = Category.objects.create(topic='Art')
category3 = Category.objects.create(topic='Science')
category4 = Category.objects.create(topic='Politics')

article1 = Post.objects.create(author=author1, type='AR', heading='Article 1', body='Article Body 1', rating=0)
PostCategory.objects.create(post=article1, category=category1)
PostCategory.objects.create(post=article1, category=category2)

article2 = Post.objects.create(author=author1, type='AR', heading='News 1', body='News Body 1', rating=0)
PostCategory.objects.create(post=article2, category=category3)
PostCategory.objects.create(post=article2, category=category4)

news1 = Post.objects.create(author=author2, type='NW', heading='News 2', body='News Body 2', rating=0)
PostCategory.objects.create(post=news1, category=category1)

comment1 = Comment.objects.create(comment='Comment 1', user=user1, post=article1, rating=0)
comment2 = Comment.objects.create(comment='Comment 2', user=user2, post=article2, rating=0)
comment3 = Comment.objects.create(comment='Comment 3', user=user1, post=news1, rating=0)
comment4 = Comment.objects.create(comment='Comment 4', user=user2, post=article1, rating=0)

comment1.like()
comment2.like()
comment3.like()
comment4.like()
comment1.like()
comment2.like()
comment3.like()
comment4.like()
comment1.dislike()
comment2.dislike()

article1.like()
article1.like()

article2.like()
news1.like()
news1.like()
news1.dislike()

author1.update_rating()
author2.update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_authors = Author.objects.all().order_by('-rating').values('user__username', 'rating')
print('Лучший пользователь - ', best_authors[0].get('user__username'), 'с рейтингом', best_authors[0].get('rating'))

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках
# к этой статье.
articles_list = Post.objects.all().order_by('-rating')
articles = articles_list.values('time_create', 'author__user__username', 'rating', 'heading')
print('Лучшая статья - пользователя ', articles[0].get('author__user__username'), 'рейтинг-', articles[0].get('rating'))
print('Заголовок статьи и дата создания- ', articles[0].get('heading'),
      articles[0].get('time_create').strftime('- %m/%d/%y %H:%M:%S'))
print('Краткое содержимое - ', articles_list[0].preview())

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье
comments = Comment.objects.filter(post=articles_list[0]).values('time_create', 'user', 'comment', 'rating')
for comment in comments:
    print('Комментарий к статье пользлователя', comment.get('user'), 'от',
          comment.get('time_create').strftime('%m/%d/%y %H:%M:%S'),
          'с рейтингом', comment.get('rating'))
    print(comment.get('comment'))




