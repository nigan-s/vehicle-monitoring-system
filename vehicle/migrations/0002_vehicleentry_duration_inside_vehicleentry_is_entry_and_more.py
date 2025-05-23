# Generated by Django 5.2 on 2025-05-02 04:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicleentry',
            name='duration_inside',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicleentry',
            name='is_entry',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='vehicleentry',
            name='paired_entry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicle.vehicleentry'),
        ),
    ]
