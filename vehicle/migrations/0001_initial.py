# Generated by Django 5.2 on 2025-04-24 06:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('vehicle_id', models.AutoField(primary_key=True, serialize=False)),
                ('registration_number', models.CharField(max_length=50, unique=True)),
                ('vehicle_type', models.CharField(choices=[('car', 'Car'), ('bike', 'Bike'), ('truck', 'Truck'), ('bus', 'Bus'), ('other', 'Other')], max_length=20)),
                ('is_authorized', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleEntry',
            fields=[
                ('entry_id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('image_url', models.URLField(max_length=255)),
                ('plate_number_detected', models.CharField(max_length=50)),
                ('confidence_score', models.FloatField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_entries', to='nodes.node')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entries', to='vehicle.vehicle')),
            ],
            options={
                'verbose_name_plural': 'Vehicle Entries',
            },
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('alert_id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_type', models.CharField(choices=[('unauthorized', 'Unauthorized Vehicle'), ('suspicious', 'Suspicious Activity'), ('unrecognized', 'Unrecognized Plate'), ('other', 'Other')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='vehicle.vehicleentry')),
            ],
        ),
    ]
