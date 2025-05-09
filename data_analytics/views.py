# vehicle/views/insights.py

from django.utils.timezone import now, timedelta
from django.db.models import Count, Q, Avg, DurationField, ExpressionWrapper, F, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vehicle.models import Vehicle, VehicleEntry, Alert
from datetime import datetime
from collections import defaultdict

class InsightsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        last_30_days = today - timedelta(days=30)

        # 1. Daily Entry and Exit Trends
        daily_stats = []
        for i in range(30):
            day = today - timedelta(days=i)
            entries = VehicleEntry.objects.filter(timestamp__date=day, is_entry=True).count()
            exits = VehicleEntry.objects.filter(timestamp__date=day, is_entry=False).count()
            daily_stats.append({
                "date": day.isoformat(),
                "entries": entries,
                "exits": exits
            })
        daily_stats.reverse()

        # 2. Vehicle Type Distribution
        type_distribution = dict(Vehicle.objects.values_list('vehicle_type').annotate(count=Count('vehicle_id')))

        # 3. Unauthorized Vehicle Attempts
        unauthorized_attempts = []
        for i in range(30):
            day = today - timedelta(days=i)
            count = Alert.objects.filter(alert_type='unauthorized', created_at__date=day).count()
            unauthorized_attempts.append({
                "date": day.isoformat(),
                "unauthorized_attempts": count
            })
        unauthorized_attempts.reverse()

        # 4. Top 50 Vehicles with Highest Total In-Time
        top_vehicles = []
        authorized_entries = VehicleEntry.objects.filter(is_entry=False, paired_entry__isnull=False, timestamp__date__gte=last_30_days)
        durations = authorized_entries.annotate(duration=ExpressionWrapper(
            F('timestamp') - F('paired_entry__timestamp'),
            output_field=DurationField()
        )).values('vehicle__registration_number').annotate(
            total_time=Sum('duration')
        ).order_by('-total_time')[:50]

        for record in durations:
            top_vehicles.append({
                "registration_number": record['vehicle__registration_number'],
                "total_time_minutes": round(record['total_time'].total_seconds() / 60, 2)
            })

        # 5. Hour-wise Vehicle Count (Current Day)
        hour_stats = defaultdict(int)
        entries_today = VehicleEntry.objects.filter(timestamp__date=today, is_entry=True)
        for entry in entries_today:
            hour = entry.timestamp.hour
            hour_stats[f"{hour:02d}:00"] += 1

        hour_graph_data = [{"hour": hour, "vehicles": count} for hour, count in sorted(hour_stats.items())]

        return Response({
            "daily_stats": daily_stats,
            "vehicle_type_distribution": type_distribution,
            "unauthorized_attempts": unauthorized_attempts,
            "top_vehicles_by_time": top_vehicles,
            "hour_wise_vehicle_count": hour_graph_data
        })
