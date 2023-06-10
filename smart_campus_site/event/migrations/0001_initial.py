# Generated by Django 3.2.6 on 2023-06-09 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='venue_event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('event', models.CharField(max_length=10)),
                ('instructor', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name_plural': 'venue_events',
            },
        ),
    ]
