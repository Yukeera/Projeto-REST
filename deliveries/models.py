import uuid
from django.db import models
from vehicles.models import Vehicle


class Delivery(models.Model):
    STATUS_CHOICES = [
        ('created', 'Criada'),
        ('in_transit', 'Em trânsito'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelada'),
    ]

    tracking_code = models.CharField(max_length=20, unique=True, blank=True)
    origin_address = models.CharField(max_length=255)
    destination_address = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)
    cargo_weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = f"TRK{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_code} - {self.recipient_name}"
