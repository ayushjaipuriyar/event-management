# Generated by Django 4.2.3 on 2023-07-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_event_end_time_alter_event_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.EmailField(default=None, max_length=254, null=True),
        ),
    ]
