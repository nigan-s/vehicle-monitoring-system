# Generated by Django 5.2 on 2025-05-09 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0002_vehicleentry_duration_inside_vehicleentry_is_entry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleentry',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
