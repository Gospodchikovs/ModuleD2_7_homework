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

news1 = Post.objects.create(author=author1, type='NW', heading='News 1', body='News Body 1', rating=0)
PostCategory.objects.create(post=news1, category=category3)
PostCategory.objects.create(post=news1, category=category4)

news2 = Post.objects.create(author=author2, type='NW', heading='News 2', body='News Body 2', rating=0)
PostCategory.objects.create(post=news2, category=category1)

comment1 = Comment.objects.create(comment='Comment 1', user=user1, post=article1, rating=0)
comment2 = Comment.objects.create(comment='Comment 2', user=user2, post=news1, rating=0)
comment3 = Comment.objects.create(comment='Comment 3', user=user1, post=news2, rating=0)
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

news1.like()
news2.like()
news2.like()
news2.dislike()

author1.update_rating()
author2.update_rating()
