# vehicle/management/commands/generate_fake_entries.py

import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from vehicle.models import Vehicle, VehicleEntry
from nodes.models import Node
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake vehicle entries for the past 3 months'

    def handle(self, *args, **kwargs):
        nodes = list(Node.objects.all())
        vehicle_types = ['car', 'bike', 'truck', 'bus', 'van', 'other']

        if not nodes:
            self.stdout.write(self.style.ERROR('No nodes found. Please add at least one node.'))
            return

        start_date = datetime.now() - timedelta(days=90)
        end_date = datetime.now()

        num_entries = 300

        for _ in range(num_entries):
            # Create a random vehicle
            reg_number = f"{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{random.randint(10, 99)}{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{random.randint(1000, 9999)}"
            vehicle_type = random.choice(vehicle_types)

            vehicle = Vehicle.objects.create(
                registration_number=reg_number,
                vehicle_type=vehicle_type,
                is_authorized=random.choice([True, False])
            )

            is_entry = True
            timestamp = fake.date_time_between(start_date=start_date, end_date=end_date)

            VehicleEntry.objects.create(
                vehicle=vehicle,
                timestamp=timestamp,
                image_url=fake.image_url(),
                plate_number_detected=reg_number,
                confidence_score=round(random.uniform(0.7, 0.99), 2),
                device=random.choice(nodes),
                is_entry=is_entry,
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_entries} fake vehicle entries.'))
