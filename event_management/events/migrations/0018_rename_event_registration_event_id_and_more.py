# Generated by Django 4.2.3 on 2023-07-05 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_alter_event_venue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='event',
            new_name='event_id',
        ),
        migrations.RenameField(
            model_name='registration',
            old_name='user',
            new_name='user_id',
        ),
    ]
