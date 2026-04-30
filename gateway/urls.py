from django.urls import path
from .views import (
    GatewayDeliveryListView,
    GatewayDeliveryDetailView,
    GatewayDeliveryActionView,
    GatewayVehicleListView,
    GatewayVehicleDetailView,
    GatewayDriverListView,
    GatewayDriverDetailView,
)

urlpatterns = [
    # Deliveries
    path('deliveries/', GatewayDeliveryListView.as_view(), name='gateway-delivery-list'),
    path('deliveries/<int:pk>/', GatewayDeliveryDetailView.as_view(), name='gateway-delivery-detail'),
    path('deliveries/<int:pk>/<str:action>/', GatewayDeliveryActionView.as_view(), name='gateway-delivery-action'),

    # Vehicles
    path('vehicles/', GatewayVehicleListView.as_view(), name='gateway-vehicle-list'),
    path('vehicles/<int:pk>/', GatewayVehicleDetailView.as_view(), name='gateway-vehicle-detail'),

    # Drivers
    path('drivers/', GatewayDriverListView.as_view(), name='gateway-driver-list'),
    path('drivers/<int:pk>/', GatewayDriverDetailView.as_view(), name='gateway-driver-detail'),
]
