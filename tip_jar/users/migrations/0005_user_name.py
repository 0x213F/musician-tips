# Generated by Django 3.0.10 on 2020-11-13 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201113_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='Josh', max_length=280),
            preserve_default=False,
        ),
    ]
