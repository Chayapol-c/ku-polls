# Generated by Django 3.1 on 2020-09-17 06:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 18, 5, 27, 32, 624103, tzinfo=utc), verbose_name='ending date '),
            preserve_default=False,
        ),
    ]