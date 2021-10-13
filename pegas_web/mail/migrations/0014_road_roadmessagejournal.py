# Generated by Django 3.2.7 on 2021-10-08 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0013_alter_file_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadMessageJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('message_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='message_id', to='mail.message')),
                ('next_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='next_user', to=settings.AUTH_USER_MODEL)),
                ('prev_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='prev_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Road',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('user_in_route', models.ManyToManyField(related_name='user_road', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]