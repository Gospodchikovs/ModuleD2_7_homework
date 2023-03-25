import datetime
import logging
from news.models import Post, Subscriber, Category, PostCategory  # pycharm подсвечитвает красным, но все работает.
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
logger = logging.getLogger(__name__)


def my_job():
    control_date = timezone.now() - datetime.timedelta(days=7)  # отматываем неделю назад
    all_subscribers = Subscriber.objects.all().values('user', 'user__username', 'user__email').distinct()
    for subscriber in all_subscribers:
        if (subscriber['user__email'] == ''):  # у пользователя нет Email, переходим к следующему
            continue
        news = []  # формируем список новостей за неделю по конкретной категории ипользователю
        news_text = ''  # текстовая версия списка новостей
        users_categories = Subscriber.objects.filter(user=subscriber['user']).values('category').distinct()
        for category in users_categories:   # перебьираем все категории, на которые полписан пользователь
            posts = Post.objects.filter(category=category['category'], time_create__gt=control_date)
            for post in posts:
                post.url_for_letter = 'http://' + Site.objects.get_current().domain + ':8000/' + str(post.id) + '/'
                news.append(post)
                news_text += f'Новость - {post.heading} / {post.body[:30]} : {post.url_for_letter} \n'
        html_content = render_to_string('letter_week.html', {'news': news})
        msg = EmailMultiAlternatives(
            subject=f'Новости за неделю для {subscriber["user__username"]}',
            body=news_text,
            from_email='s.gospodchikov@yandex.ru',
            to=[subscriber['user__email']],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),  # отправка писем раз в неделю
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
