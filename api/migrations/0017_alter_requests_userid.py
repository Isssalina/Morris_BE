# Generated by Django 3.2.12 on 2022-03-16 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_healthcareprofessional_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='userID',
            field=models.ForeignKey(blank=True, db_column='userID', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.users'),
        ),
    ]
