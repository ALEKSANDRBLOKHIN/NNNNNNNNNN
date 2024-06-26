# Generated by Django 5.0.4 on 2024-04-18 23:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_list', '0003_alter_post_post_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribed_categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
