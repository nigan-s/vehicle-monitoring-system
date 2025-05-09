from rest_framework import generics, permissions
from vehicle.models import VehicleEntry
from vehicle.serializers import VehicleEntrySerializer

class VehicleEntryCreateView(generics.CreateAPIView):
    queryset = VehicleEntry.objects.all()
    serializer_class = VehicleEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        instance = serializer.save()
        
        # If this is an exit record
        if not instance.is_entry and instance.vehicle:
            # Find the latest unmatched entry for this vehicle
            unmatched_entry = VehicleEntry.objects.filter(
                vehicle=instance.vehicle,
                is_entry=True,
                paired_entry__isnull=True
            ).order_by('-timestamp').first()
            
            if unmatched_entry:
                # Calculate duration
                duration = instance.timestamp - unmatched_entry.timestamp
                instance.duration_inside = duration
                instance.paired_entry = unmatched_entry
                instance.save()

                # Update the original entry to link back to this exit
                unmatched_entry.paired_entry = instance
                unmatched_entry.save()