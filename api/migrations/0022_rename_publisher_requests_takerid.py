# Generated by Django 3.2.12 on 2022-03-17 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_requests_publisher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requests',
            old_name='publisher',
            new_name='takerID',
        ),
    ]
