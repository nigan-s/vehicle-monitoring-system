from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class AuthorizedVehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

class BlacklistVehicleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plate_number = request.data.get('registration_number')

        if not plate_number:
            return Response({"error": "registration_number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vehicle = Vehicle.objects.get(registration_number=plate_number)
            vehicle.is_authorized = False
            vehicle.save()
            return Response({"message": f"Vehicle {plate_number} has been blacklisted."})
        except Vehicle.DoesNotExist:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)