from rest_framework import generics, permissions
from vehicle.models import VehicleEntry
from vehicle.serializers import VehicleEntrySerializer
from rest_framework.response import Response
from django.db.models import Q

class VehicleLogListView(generics.ListAPIView):
    queryset = VehicleEntry.objects.select_related('vehicle', 'device').all().order_by('-timestamp')
    serializer_class = VehicleEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        # Optional filter by role
        if user.role == 'viewer':
            return qs[:100]  # limit for viewers
        return qs


class CurrentVehiclesView(generics.ListAPIView):
    serializer_class = VehicleEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VehicleEntry.objects.filter(
            is_entry=True,
            paired_entry__isnull=True
        ).select_related('vehicle', 'device').order_by('-timestamp')
