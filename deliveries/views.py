from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Delivery
from .serializers import DeliverySerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        delivery = self.get_object()

        if delivery.status != 'created':
            return Response(
                {'error': f'Não é possível iniciar uma entrega com status "{delivery.status}".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not delivery.vehicle:
            return Response(
                {'error': 'É necessário atribuir um veículo antes de iniciar a entrega.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        delivery.status = 'in_transit'
        delivery.started_at = timezone.now()
        delivery.save()

        return Response(DeliverySerializer(delivery).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        delivery = self.get_object()

        if delivery.status != 'in_transit':
            return Response(
                {'error': f'Apenas entregas em trânsito podem ser concluídas. Status atual: "{delivery.status}".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        delivery.status = 'delivered'
        delivery.delivered_at = timezone.now()
        delivery.save()

        return Response(DeliverySerializer(delivery).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        delivery = self.get_object()

        if delivery.status == 'delivered':
            return Response(
                {'error': 'Não é possível cancelar uma entrega já concluída.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        delivery.status = 'cancelled'
        delivery.save()

        return Response(DeliverySerializer(delivery).data)
