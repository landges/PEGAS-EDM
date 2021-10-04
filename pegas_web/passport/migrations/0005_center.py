# Generated by Django 3.2.7 on 2021-09-28 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passport', '0004_delete_center'),
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=100)),
                ('public_key', models.FileField(blank=True, default=None, null=True, upload_to='keys/')),
            ],
        ),
    ]
