# Generated by Django 3.2.7 on 2021-10-15 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passport', '0003_center'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='private_key',
            field=models.BinaryField(null=True),
        ),
    ]
