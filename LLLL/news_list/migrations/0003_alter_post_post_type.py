# Generated by Django 5.0.4 on 2024-04-18 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_list', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('NE', 'News'), ('AR', 'Article')], default='NE', max_length=2),
        ),
    ]