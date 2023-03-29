from django.core.management.base import BaseCommand, CommandError
from news.models import Post, PostCategory


class Command(BaseCommand):
    help = 'Удаление всех новстей'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True

    def handle(self, *args, **options):
        categories_list = PostCategory.objects.all()
        self.stdout.readable()
        self.stdout.write('Выберите код категории для удаления')
        for category in categories_list.values('category', 'category__topic').order_by('category').distinct():
            self.stdout.write(f"{category['category']} - {category['category__topic']}")
        try:
            category_for_del = int(input())
        except ValueError:
            self.stdout.write(self.style.ERROR('Ошиька ввода категории! Удаление не произведено.'))
        else:
            if categories_list.filter(category_id=category_for_del).exists():
                self.stdout.write('Вы действительно хотите удалить все новости выбранной категории? yes/No')
                if input() == 'yes':
                    Post.objects.filter(category__id=category_for_del).delete()
                    self.stdout.write(self.style.SUCCESS('Успешное удаление новстей!'))
                    return
            self.stdout.write(self.style.ERROR('Удаление не произведено!'))
        return
