# Generated by Django 3.0.10 on 2020-11-15 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_amountchoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=0, max_digits=6),
        ),
    ]
