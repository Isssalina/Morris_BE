# Generated by Django 3.2.12 on 2022-04-07 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20220407_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='workrecord',
            name='hcpPayed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='workrecord',
            name='salary',
            field=models.FloatField(default=100),
        ),
        migrations.AlterField(
            model_name='workrecord',
            name='hasPayed',
            field=models.BooleanField(default=False),
        ),
    ]
