import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category, SubAuthor, Author

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    f = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    r = datetime.datetime.utcnow()
    cat = Category.objects.all()
    print('ok')
    for item in cat:
        print(item)
        c = Post.objects.filter(create__range=(f, r), category=item)
        p = SubAuthor.objects.filter(category2__name=item)
        mails = []
        print(c,p)
        for i in p:
            print(i.author2.user.email)
            if len(i.author2.user.email) > 1:
                mails.append(str(i.author2.user.email))
        print(mails, item)
        html_content = render_to_string('newslist.html',{'newslist': c})
        msg = EmailMultiAlternatives(
            subject=item,
            body='list',
            from_email='olevova1983@gmail.com',
            to=mails,)
        msg.attach_alternative(html_content, "text/html")
        msg.send()



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
            trigger=CronTrigger(week="*/1"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
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