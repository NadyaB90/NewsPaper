from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
import datetime as DT
from datetime import timedelta


def weekly_digest():
    categories = Category.objects.all()
    today = DT.datetime.today()
    week_ago = today - DT.timedelta(days=7)
    week = timedelta(days=7)
    print(today)
    print(week_ago)
    print(week)

    for category in categories:
        category_subscribers = category.subscribers.all()
        category_subscribers_emails = []
        for subscriber in category_subscribers:
            category_subscribers_emails.append(subscriber.email)
        weekly_posts_in_category = []
        posts_in_category = Post.objects.all().filter(post_category=f'{category.id}')

        print(f'ID: {category.id}')
        print(category)
        print(f'Кол-во публикаций: {len(weekly_posts_in_category)}')
        print(category_subscribers_emails)
        print(weekly_posts_in_category)

        if category_subscribers_emails:
            msg = EmailMultiAlternatives(
                subject=f'Weekly digest for subscribed category "{category}" from News Portal.',
                body=f'Здравствуй! Еженедельная подборка публикаций в выбранной категории "{category}"',
                from_email='lady.nadya20@mail.ru',
                to=category_subscribers_emails,
            )

            html_content = render_to_string(
                'weekly digest.html',
                {
                    'digest': weekly_posts_in_category,
                    'category': category,
                }
            )

            msg.attach_alternative(html_content, "text/html")

            msg.send()
        else:
            continue
