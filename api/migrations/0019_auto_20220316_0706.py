# Generated by Django 3.2.12 on 2022-03-16 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20220316_0705'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='startDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requests',
            name='endTime',
            field=models.TimeField(blank=True, db_column='endTime', null=True),
        ),
        migrations.AlterField(
            model_name='requests',
            name='startTime',
            field=models.TimeField(blank=True, db_column='startTime', null=True),
        ),
    ]
