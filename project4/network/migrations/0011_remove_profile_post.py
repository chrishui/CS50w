# Generated by Django 3.1.7 on 2021-04-22 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20210422_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='post',
        ),
    ]
