# Generated by Django 4.2.3 on 2023-07-04 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_alter_venue_name'),
        ('events', '0015_event_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='venues.venue'),
        ),
    ]
