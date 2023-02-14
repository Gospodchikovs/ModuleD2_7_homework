from news.models import Category, PostCategory, Post, Author, Comment
from django.contrib.auth.models import User

# 1.Создать двух пользователей (с помощью метода User.objects.create_user).
user1 = User.objects.create_user(username='user1', email='user1@e.mail', password='user1_password')
user2 = User.objects.create_user(username='user2', email='user2@e.mail', password='user2_password')

# 2.Создать два объекта модели Author, связанные с пользователями.
author1 = Author.objects.create(user=user1, rating=0)
author2 = Author.objects.create(user=user2, rating=0)

# 3.Добавить 4 категории в модель Category.
category1 = Category.objects.create(topic='Sport')
category2 = Category.objects.create(topic='Art')
category3 = Category.objects.create(topic='Science')
category4 = Category.objects.create(topic='Politics')

# 4.Добавить 2 статьи и 1 новость.
article1 = Post.objects.create(author=author1, type='AR', heading='Article 1', body='Article Body 1', rating=0)
article2 = Post.objects.create(author=author1, type='AR', heading='Article 2', body='Article Body 2', rating=0)
news1 = Post.objects.create(author=author2, type='NW', heading='News 2', body='News Body 1', rating=0)

# 5.Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
PostCategory.objects.create(post=article1, category=category1)
PostCategory.objects.create(post=article1, category=category2)
PostCategory.objects.create(post=article2, category=category3)
PostCategory.objects.create(post=article2, category=category4)
PostCategory.objects.create(post=news1, category=category1)

# 6.Создать как минимум 4 комментария к объектам модели Post (в каждом объекте должен быть как минимум один комментарий)
comment1 = Comment.objects.create(comment='Comment 1', user=user1, post=article1, rating=0)
comment2 = Comment.objects.create(comment='Comment 2', user=user2, post=article2, rating=0)
comment3 = Comment.objects.create(comment='Comment 3', user=user1, post=news1, rating=0)
comment4 = Comment.objects.create(comment='Comment 4', user=user2, post=article1, rating=0)

# 7.Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
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

# 8.Обновить рейтинги пользователей.
author1.update_rating()
author2.update_rating()

# 9.Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_author = Author.objects.all().order_by('-rating').values('user__username', 'rating')[0]    # берем только первого
print('Лучший пользователь - ', best_author['user__username'], 'с рейтингом', best_author['rating'])

# 10.Вывести дату, username, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
best_post = Post.objects.all().order_by('-rating')
best_post_fields = best_post.values('time_create', 'author__user__username', 'rating', 'heading')[0]
print('Лучшая статья-пользователя ', best_post_fields['author__user__username'],
      'рейтинг-', best_post_fields['rating'])
print('Заголовок статьи и дата создания- ', best_post_fields['heading'],
      best_post_fields['time_create'].strftime('- %m/%d/%y %H:%M:%S'))
print('Краткое содержимое - ', best_post[0].preview())

# 11.Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье
comments = Comment.objects.filter(post=best_post[0]).values('time_create', 'user__username', 'comment', 'rating')
for comment in comments:
    print('Комментарий к статье пользователя', comment['user__username'], 'от',
          comment['time_create'].strftime('%m/%d/%y %H:%M:%S'),
          'с рейтингом', comment['rating'], '\n', comment['comment'])
