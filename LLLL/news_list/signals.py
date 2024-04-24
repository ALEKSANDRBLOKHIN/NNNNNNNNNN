from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import UserProfile,Post
from django.core.mail import send_mail
from django.urls import reverse

@receiver(post_save, sender=User)
def add_to_common_group(sender, instance, created, **kwargs):
    if created:  # Проверяем, что это создание нового пользователя, а не обновление
        group = Group.objects.get(name='common')
        instance.groups.add(group)
        print(f'Пользователь {instance.username} добавлен в группу {group.name}')




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f'Создание профиля пользователя {instance.username}')
        UserProfile.objects.create(user=instance)
        print(f'Профиль пользователя {instance.username} создан')



@receiver(post_save, sender=Post)
def send_notification_to_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type == Post.ARTICLE:  # Ensure it's a new article
        subscribers = instance.categories.first().subscribers.all()  # Assuming the article is linked to categories
        for user in subscribers:
            subject = f"New article in {instance.categories.first().name}"
            message = f"Hello, {user.username}! A new article '{instance.title}' has been posted in {instance.categories.first().name}. " \
                      f"Read its preview here: {instance.preview()}... " \
                      f"Click the link to read the full article: http://yourdomain.com{reverse('article_detail', kwargs={'pk': instance.pk})}"
            from_email = 'from@example.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)