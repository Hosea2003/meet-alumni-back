# Generated by Django 4.1.7 on 2023-03-30 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_college_contact_alter_user_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='admin',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='college', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CollegeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isAlumni', models.BooleanField(default=False)),
                ('isConfirmed', models.BooleanField(default=False)),
                ('dateRequested', models.DateTimeField(default=django.utils.timezone.now)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.college')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colleges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
