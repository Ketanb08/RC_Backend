# Generated by Django 5.0.1 on 2024-03-05 11:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rc_app', '0015_progress_lifeline1_progress_lifeline2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='responses',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='progress',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 5, 11, 3, 12, 13328, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='progress',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 5, 11, 3, 12, 13328, tzinfo=datetime.timezone.utc)),
        ),
    ]
