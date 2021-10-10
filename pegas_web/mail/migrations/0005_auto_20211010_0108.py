# Generated by Django 3.2.7 on 2021-10-10 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0004_alter_message_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_deleted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='spam',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
