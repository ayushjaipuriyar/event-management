# Generated by Django 4.2.3 on 2023-07-04 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_venue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='venue',
        ),
    ]
