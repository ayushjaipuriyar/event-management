# Generated by Django 4.2.3 on 2023-07-04 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_delete_venue_remove_event_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]