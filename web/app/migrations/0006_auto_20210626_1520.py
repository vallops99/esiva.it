# Generated by Django 3.2.4 on 2021-06-26 15:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 6, 26, 15, 20, 21, 634424, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audio',
            name='downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
