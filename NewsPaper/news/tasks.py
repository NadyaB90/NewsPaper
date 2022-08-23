from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from celery import shared_task
from .models import Post, Category
import datetime as DT
from datetime import timedelta


@shared_task
def subscribe_category_confirmation_message(user_name, email, category_name):
    send_mail(
        subject=f'News Portal: подписка на обновления категории {category_name}',
        message=f'«{user_name}», вы подписались на обновления категории: «{category_name}».',
        from_email='lady.nadya20@mail.ru',
        recipient_list=[f'{email}', ],
    )


@shared_task
def notify_subs(sub_name, sub_email, title, category, pub_time, pk):
    post = Post.objects.get(id=pk)
    subject = f'{sub_name}, новая публикация в разделе {category} - {title},  ... {pub_time}'

    msg = EmailMultiAlternatives(
        subject=subject,
        body=f'Привет {sub_name}, новая публикация - {title}, в разделе {category}',
        from_email='lady.nadya20@mail.ru',
        to=[f'{sub_email}'],
    )

    html_content = render_to_string(
        'post_created.html',
        {
            'post': post,
            'user': sub_name,
        }
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()

    print(subject)
    print(sub_email)


@shared_task
def weekly_digest():
    categories = Category.objects.all()
    today = DT.datetime.today()
    week = timedelta(days=7)

    for category in categories:
        category_subscribers = category.subscribers.all()
        category_subscribers_emails = []
        for subscriber in category_subscribers:
            category_subscribers_emails.append(subscriber.email)

        weekly_posts_in_category = []
        posts_in_category = Post.objects.all().filter(post_category=f'{category.id}')

        for post in posts_in_category:
            time_delta = DT.datetime.now() - post.pubDate
            if time_delta < week:
                weekly_posts_in_category.append(post)

        print(f'ID: {category.id}')
        print(category)
        print(f'Кол-во публикаций: {len(weekly_posts_in_category)}')
        print(category_subscribers_emails)
        print(weekly_posts_in_category)

        if category_subscribers_emails:
            msg = EmailMultiAlternatives(
                subject=f'Weekly digest for subscribed category "{category}" from NewsPaper.',
                body=f'Привет! Еженедельная подборка публикаций в выбранной категории "{category}"',
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