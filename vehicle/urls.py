from django.urls import path
from vehicle.views.entry import VehicleEntryCreateView
from vehicle.views.logs import VehicleLogListView, CurrentVehiclesView
from vehicle.views.vehicle import AuthorizedVehicleListCreateView, BlacklistVehicleView
from vehicle.views.alert import AlertListView


urlpatterns = [
    path('vehicle-entry/', VehicleEntryCreateView.as_view(), name='vehicle-entry'),
    path('vehicle-logs/', VehicleLogListView.as_view(), name='vehicle-logs'),
    path('current-vehicles/', CurrentVehiclesView.as_view(), name='current-vehicles'),
    path('authorized-vehicles/', AuthorizedVehicleListCreateView.as_view()),
    path('blacklist-vehicle/', BlacklistVehicleView.as_view()),
    path('alerts/', AlertListView.as_view()),

]
