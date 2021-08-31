# Generated by Django 3.2.6 on 2021-08-31 18:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210825_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='liked_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]
