# Generated by Django 3.0.10 on 2020-11-13 08:20

from django.db import migrations, models
import tip_jar.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_img',
            field=models.FileField(blank=True, null=True, upload_to=tip_jar.users.models.upload_to_comments_voice_recordings),
        ),
    ]