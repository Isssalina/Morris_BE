# Generated by Django 3.2.12 on 2022-04-07 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_requests_hourlyrate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScheduleRecord',
            new_name='WorkRecord',
        ),
        migrations.AlterModelTable(
            name='workrecord',
            table='WorkRecord',
        ),
    ]
