from django.db import models


class Driver(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('on_route', 'Em rota'),
        ('unavailable', 'Indisponível'),
    ]

    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.license_number})"


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('in_use', 'Em uso'),
        ('maintenance', 'Em manutenção'),
    ]

    license_plate = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    cargo_capacity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.license_plate} - {self.model}"
