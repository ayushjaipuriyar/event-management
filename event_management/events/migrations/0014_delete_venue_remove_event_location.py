# Generated by Django 4.2.3 on 2023-07-04 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_event_creator'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Venue',
        ),
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
    ]
