# Generated by Django 3.1.5 on 2021-01-22 20:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_remove_message_is_readed'),
    ]

    operations = [
        migrations.CreateModel(
            name='BAN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ban', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Участник')),
            ],
        ),
    ]
