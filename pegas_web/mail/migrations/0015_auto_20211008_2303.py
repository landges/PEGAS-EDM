# Generated by Django 3.2.7 on 2021-10-08 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0014_road_roadmessagejournal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='draft',
        ),
        migrations.AlterField(
            model_name='message',
            name='in_route',
            field=models.BooleanField(default=False),
        ),
    ]