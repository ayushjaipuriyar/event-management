# Generated by Django 4.2.3 on 2023-07-04 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
