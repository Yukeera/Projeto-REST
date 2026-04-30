from rest_framework import serializers
from .models import Driver, Vehicle


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'name', 'license_number', 'phone', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class VehicleSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'license_plate', 'model', 'year', 'cargo_capacity_kg',
            'status', 'driver', 'driver_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
