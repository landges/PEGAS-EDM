# Generated by Django 3.2.7 on 2021-10-11 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0017_remove_road_user_in_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='draft',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
