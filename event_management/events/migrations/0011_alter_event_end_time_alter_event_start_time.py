# Generated by Django 4.2.3 on 2023-07-04 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_event_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]