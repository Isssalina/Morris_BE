# Generated by Django 3.2.12 on 2022-04-11 09:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20220410_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcareprofessional',
            name='billingAccount',
            field=models.JSONField(default={'paidTotal': 0.0, 'total': 0.0, 'unPaidTotal': 0.0}),
        ),
        migrations.AddField(
            model_name='requests',
            name='billingAccount',
            field=models.JSONField(default={'paidTotal': 0.0, 'total': 0.0, 'unPaidTotal': 0.0}),
        ),
        migrations.AlterField(
            model_name='payrecord',
            name='paidTime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]