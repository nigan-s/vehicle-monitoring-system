from django.db import models
from django.core.validators import validate_ipv46_address

class Node(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    ]
    
    device_id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(validators=[validate_ipv46_address])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    last_seen = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.display_name} ({self.location_name})"
