from django.db import models
from nodes.models import Node

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('truck', 'Truck'),
        ('bus', 'Bus'),
        ('other', 'Other'),
    ]
    
    vehicle_id = models.AutoField(primary_key=True)
    registration_number = models.CharField(max_length=50, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    is_authorized = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.registration_number} ({self.vehicle_type})"

class VehicleEntry(models.Model):
    entry_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='entries')
    timestamp = models.DateTimeField()
    image_url = models.URLField(max_length=255)
    plate_number_detected = models.CharField(max_length=50)
    confidence_score = models.FloatField()
    device = models.ForeignKey('nodes.Node', on_delete=models.CASCADE, related_name='vehicle_entries')
    
    is_entry = models.BooleanField(default=True)  # True = Entry, False = Exit
    paired_entry = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)  # for exits
    duration_inside = models.DurationField(null=True, blank=True)  # computed on exit

    def __str__(self):
        direction = "IN" if self.is_entry else "OUT"
        return f"{self.plate_number_detected} [{direction}] at {self.timestamp}"
    
    class Meta:
        verbose_name_plural = "Vehicle Entries"

class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('unauthorized', 'Unauthorized Vehicle'),
        ('suspicious', 'Suspicious Activity'),
        ('unrecognized', 'Unrecognized Plate'),
        ('other', 'Other'),
    ]
    
    alert_id = models.AutoField(primary_key=True)
    entry = models.ForeignKey(VehicleEntry, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.alert_type} alert for entry {self.entry_id}"
