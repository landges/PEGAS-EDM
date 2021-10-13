# Generated by Django 3.2.7 on 2021-10-08 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0009_alter_road_route'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='road',
            name='route',
        ),
        migrations.AddField(
            model_name='message',
            name='in_route',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='road',
            name='user_in_route',
            field=models.ManyToManyField(related_name='user_road', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RoadMessageJournal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('message_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='message_id', to='mail.message')),
                ('next_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='next', to=settings.AUTH_USER_MODEL)),
                ('prev_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='prev', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]