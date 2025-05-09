from rest_framework import serializers
from .models import VehicleEntry, Vehicle
from nodes.models import Node
from vehicle.models import Alert

class VehicleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleEntry
        fields = '__all__'

    def create(self, validated_data):
        plate_number = validated_data.get('plate_number_detected')
        vehicle = Vehicle.objects.filter(registration_number=plate_number).first()

        if not vehicle:
            # Create unknown vehicle if not found
            vehicle = Vehicle.objects.create(
                registration_number=plate_number,
                vehicle_type='other',
                is_authorized=False
            )

        # Attach the vehicle to validated_data
        validated_data['vehicle'] = vehicle

        # Create the VehicleEntry
        instance = super().create(validated_data)

        # Handle exit duration and pairing
        if not instance.is_entry:
            last_entry = VehicleEntry.objects.filter(
                vehicle=instance.vehicle,
                is_entry=True,
                paired_entry__isnull=True
            ).order_by('-timestamp').first()

            if last_entry:
                instance.duration_inside = instance.timestamp - last_entry.timestamp
                instance.paired_entry = last_entry
                instance.save()

                last_entry.paired_entry = instance
                last_entry.save()

        return instance


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
