# Generated by Django 4.1.7 on 2023-03-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='contact',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact',
            field=models.CharField(default='034 30 799 19', max_length=15),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
