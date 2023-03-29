from django.core.management.base import BaseCommand, CommandError
from news.models import Post, PostCategory


class Command(BaseCommand):
    help = 'Удаление всех новстей'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)
    def handle(self, *args, **options):
        self.stdout.readable()
        categories_list = PostCategory.objects.all().order_by('category')\
            .values('category', 'category__topic').distinct()
        self.stdout.write('Выберите код категории для удаления')
        cat_id = []
        for category in categories_list:
            self.stdout.write(f"{category['category']} - {category['category__topic']}")
            cat_id.append(category['category'])     # список категорий для выбора
        category_del = int(input())
        if category_del in cat_id:
            self.stdout.write('Вы действительно хотите удалить все новости выбранной категории {? yes/no')
            answer = input()
            if answer == 'yes':
                Post.objects.filter(category__id=category_del).delete()
                self.stdout.write(self.style.SUCCESS('Успешное удаление новстей!'))
                return
        self.stdout.write(self.style.ERROR('Удаление не произведено!'))
        return
