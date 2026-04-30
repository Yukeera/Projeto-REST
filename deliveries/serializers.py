from rest_framework import serializers
from .models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    vehicle_plate = serializers.CharField(source='vehicle.license_plate', read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'id', 'tracking_code', 'origin_address', 'destination_address',
            'recipient_name', 'recipient_phone', 'cargo_weight_kg',
            'vehicle', 'vehicle_plate', 'status',
            'created_at', 'started_at', 'delivered_at'
        ]
        read_only_fields = [
            'id', 'tracking_code', 'status',
            'created_at', 'started_at', 'delivered_at'
        ]
