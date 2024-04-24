# myapp/tasks.py

from .models import Category, Post
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail, send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Post
from celery import shared_task
@shared_task
def send_notification_email(user_email, subject, message):
    send_mail(
        subject,
        message,
        'from@example.com',
        [user_email],
        fail_silently=False,
    )


@shared_task
def send_weekly_news():
    week_ago = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()
    for category in categories:
        posts = Post.objects.filter(categories=category, created_at__gte=week_ago)
        if posts.exists():
            for subscriber in category.subscribers.all():
                subject = 'Weekly News Update'
                message = 'Here are the new articles from the categories you subscribe to:\n\n'
                message += '\n'.join([f"{post.title}: http://yourdomain.com{post.get_absolute_url()}" for post in posts])
                send_mail(subject, message, 'from@example.com', [subscriber.email])





@shared_task
def send_weekly_newsletter():
    last_week = timezone.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(created_at__gte=last_week)

    if not recent_posts.exists():
        return  # No new posts, no need to send emails

    # Assuming there is a field or method to get email subscribers,
    # this could be an attribute of posts or a separate subscriber model.
    messages = []
    subscribers = User.objects.filter(is_active=True)  # Assuming active users want the newsletter

    for subscriber in subscribers:
        subject = "Weekly News Update"
        message_body = "Check out the latest articles:\n\n"
        message_body += "\n".join([f"{post.title}: http://yourdomain.com{post.get_absolute_url()}" for post in recent_posts])
        message = (subject, message_body, 'from@example.com', [subscriber.email])
        messages.append(message)

    if messages:
        send_mass_mail(messages, fail_silently=False)
