# Generated by Django 4.1.7 on 2023-04-07 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.TextField(default='hey you'),
            preserve_default=False,
        ),
    ]
