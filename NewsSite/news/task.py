from datetime import datetime, timedelta
from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import *


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)
#"@shared_task
#def SendNew():
#    Nl = Post.objects.filter(create__gt = datetime.now() - timedelta(weeks=1))
#    Subs = Author.objects.filter()
#    mails = []
#    for i in Subs:
#        if len(i.user.email) > 1:
#            mails.append(str(i.user.email))
#    html_content = render_to_string(
#        'news.html',
#        {
#            'news': Nl,
#        }
#    )
#    msg = EmailMultiAlternatives(
#        subject='week news',
#        body='week news',
#        from_email = 'olevova1983@gmail.com',
#        to=mails,
#        )
#    msg.attach_alternative(html_content, "text/html")
#    msg.send()