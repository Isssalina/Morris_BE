# Generated by Django 3.2.12 on 2022-04-07 02:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20220407_0217'),
    ]

    operations = [
        migrations.AddField(
            model_name='workrecord',
            name='hcpPayedTime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='workrecord',
            name='payedTime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
