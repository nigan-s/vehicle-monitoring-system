from django.core.management.base import BaseCommand
from vehicle.models import VehicleEntry, Vehicle

class Command(BaseCommand):
    help = 'Delete all entries from Vehicle and VehicleEntry tables'

    def handle(self, *args, **kwargs):
        VehicleEntry.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All VehicleEntry records deleted'))

        Vehicle.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All Vehicle records deleted'))
