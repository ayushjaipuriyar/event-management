# Generated by Django 4.2.3 on 2023-07-04 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_alter_venue_name'),
        ('events', '0016_alter_event_creator_alter_event_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='venues.venue', to_field='name'),
        ),
    ]
