from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление всех новстей'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True

    def handle(self, *args, **options):
        categories_list = Category.objects.all()
        self.stdout.readable()
        self.stdout.write('Выберите код категории для удаления')
        for category in categories_list:
            self.stdout.write(f"{category.id} - {category.topic}")
        try:
            category_for_del = int(input())
        except ValueError:
            self.stdout.write(self.style.ERROR('Ошибка ввода категории! Удаление не произведено.'))
        else:
            if categories_list.filter(id=category_for_del).exists():
                self.stdout.write('Вы действительно хотите удалить все новости выбранной категории? yes/No')
                if input() == 'yes':
                    Post.objects.filter(category__id=category_for_del).delete()
                    self.stdout.write(self.style.SUCCESS('Успешное удалено новостей'))
                    return
            self.stdout.write(self.style.ERROR('Удаление не произведено!'))
        return
