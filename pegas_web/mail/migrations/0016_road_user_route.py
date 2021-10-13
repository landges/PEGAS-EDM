# Generated by Django 3.2.7 on 2021-10-08 22:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0015_auto_20211008_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='road',
            name='user_route',
            field=models.ManyToManyField(related_name='user_roat', to=settings.AUTH_USER_MODEL),
        ),
    ]