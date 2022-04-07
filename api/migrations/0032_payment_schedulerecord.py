# Generated by Django 3.2.12 on 2022-04-07 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_remove_requests_servicetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduleID', models.IntegerField()),
                ('workDate', models.DateField()),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('amount', models.FloatField()),
                ('hasPayed', models.BooleanField()),
                ('hcp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.healthcareprofessional')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.requests')),
            ],
            options={
                'db_table': 'ScheduleRecord',
            },
        ),
    ]
