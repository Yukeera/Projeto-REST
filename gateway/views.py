import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Endereços internos das APIs
VEHICLES_API = "http://127.0.0.1:8000/api/vehicles"
DELIVERIES_API = "http://127.0.0.1:8000/api/deliveries"


def build_delivery_links(request, delivery):
    """
    Monta os links HATEOAS de uma entrega com base no status atual.
    Apenas ações válidas para o estado atual são incluídas.
    """
    delivery_id = delivery['id']
    base = request.build_absolute_uri(f'/gateway/deliveries/{delivery_id}/')
    status_atual = delivery['status']

    links = {
        'self': base,
    }

    if status_atual == 'created':
        links['start'] = request.build_absolute_uri(f'/gateway/deliveries/{delivery_id}/start/')
        links['cancel'] = request.build_absolute_uri(f'/gateway/deliveries/{delivery_id}/cancel/')

    elif status_atual == 'in_transit':
        links['complete'] = request.build_absolute_uri(f'/gateway/deliveries/{delivery_id}/complete/')
        links['cancel'] = request.build_absolute_uri(f'/gateway/deliveries/{delivery_id}/cancel/')

    if delivery.get('vehicle'):
        links['vehicle'] = request.build_absolute_uri(f'/gateway/vehicles/{delivery["vehicle"]}/')

    return links


def build_vehicle_links(request, vehicle):
    """
    Monta os links HATEOAS de um veículo.
    """
    vehicle_id = vehicle['id']

    links = {
        'self': request.build_absolute_uri(f'/gateway/vehicles/{vehicle_id}/'),
        'deliveries': request.build_absolute_uri(f'/gateway/deliveries/'),
    }

    if vehicle.get('driver'):
        links['driver'] = request.build_absolute_uri(f'/gateway/drivers/{vehicle["driver"]}/')

    return links


# ─── GATEWAY: DELIVERIES ────────────────────────────────────────────────────

class GatewayDeliveryListView(APIView):
    """
    Endpoint de Entregas do Gateway.
    Retorna a lista de entregas com links HATEOAS para as ações disponíveis.
    """

    @swagger_auto_schema(
        operation_summary="Listar entregas",
        operation_description="Retorna todas as entregas cadastradas com links HATEOAS indicando as ações disponíveis para cada status.",
        responses={200: openapi.Response(description="Lista de entregas com links HATEOAS")}
    )
    def get(self, request):
        response = requests.get(f"{DELIVERIES_API}/deliveries/")
        deliveries = response.json()

        result = []
        for delivery in deliveries:
            delivery['links'] = build_delivery_links(request, delivery)
            result.append(delivery)

        return Response(result, status=response.status_code)

    @swagger_auto_schema(
        operation_summary="Criar entrega",
        operation_description="Cria uma nova entrega. O código de rastreamento é gerado automaticamente. Status inicial: 'created'.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['origin_address', 'destination_address', 'recipient_name', 'recipient_phone', 'cargo_weight_kg'],
            properties={
                'origin_address': openapi.Schema(type=openapi.TYPE_STRING, description='Endereço de origem'),
                'destination_address': openapi.Schema(type=openapi.TYPE_STRING, description='Endereço de destino'),
                'recipient_name': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do destinatário'),
                'recipient_phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefone do destinatário'),
                'cargo_weight_kg': openapi.Schema(type=openapi.TYPE_NUMBER, description='Peso da carga em kg'),
                'vehicle': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do veículo (opcional)'),
            }
        ),
        responses={201: openapi.Response(description="Entrega criada com sucesso")}
    )
    def post(self, request):
        response = requests.post(
            f"{DELIVERIES_API}/deliveries/",
            json=request.data
        )
        delivery = response.json()

        if response.status_code == 201:
            delivery['links'] = build_delivery_links(request, delivery)

        return Response(delivery, status=response.status_code)


class GatewayDeliveryDetailView(APIView):
    """
    Detalhes, atualização e remoção de uma entrega específica.
    """

    @swagger_auto_schema(
        operation_summary="Detalhar entrega",
        operation_description="Retorna os dados de uma entrega específica com links HATEOAS baseados no status atual.",
        responses={
            200: openapi.Response(description="Dados da entrega com links HATEOAS"),
            404: openapi.Response(description="Entrega não encontrada")
        }
    )
    def get(self, request, pk):
        response = requests.get(f"{DELIVERIES_API}/deliveries/{pk}/")
        if response.status_code == 404:
            return Response({'error': 'Entrega não encontrada.'}, status=404)

        delivery = response.json()
        delivery['links'] = build_delivery_links(request, delivery)
        return Response(delivery)

    @swagger_auto_schema(
        operation_summary="Atualizar entrega",
        operation_description="Atualiza os dados de uma entrega. Não é possível alterar o status diretamente — use os endpoints de ação (start, complete, cancel).",
        responses={200: openapi.Response(description="Entrega atualizada")}
    )
    def put(self, request, pk):
        response = requests.put(
            f"{DELIVERIES_API}/deliveries/{pk}/",
            json=request.data
        )
        delivery = response.json()
        if response.status_code == 200:
            delivery['links'] = build_delivery_links(request, delivery)
        return Response(delivery, status=response.status_code)

    @swagger_auto_schema(
        operation_summary="Remover entrega",
        operation_description="Remove uma entrega do sistema.",
        responses={204: openapi.Response(description="Entrega removida")}
    )
    def delete(self, request, pk):
        response = requests.delete(f"{DELIVERIES_API}/deliveries/{pk}/")
        return Response(status=response.status_code)


class GatewayDeliveryActionView(APIView):
    """
    Ações de transição de status de uma entrega.
    Implementa o conceito de HATEOAS — apenas ações válidas para o estado atual são permitidas.
    """

    @swagger_auto_schema(
        operation_summary="Executar ação na entrega",
        operation_description=(
            "Executa uma ação de transição de status na entrega. Ações disponíveis:\n\n"
            "- **start**: Inicia a entrega (created → in_transit). Requer veículo atribuído.\n"
            "- **complete**: Conclui a entrega (in_transit → delivered).\n"
            "- **cancel**: Cancela a entrega (created ou in_transit → cancelled)."
        ),
        responses={
            200: openapi.Response(description="Ação executada com sucesso"),
            400: openapi.Response(description="Ação inválida para o status atual"),
        }
    )
    def post(self, request, pk, action):
        valid_actions = ['start', 'complete', 'cancel']

        if action not in valid_actions:
            return Response(
                {'error': f'Ação inválida. Ações disponíveis: {valid_actions}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = requests.post(f"{DELIVERIES_API}/deliveries/{pk}/{action}/")
        delivery = response.json()

        if response.status_code == 200:
            delivery['links'] = build_delivery_links(request, delivery)

        return Response(delivery, status=response.status_code)


# ─── GATEWAY: VEHICLES ──────────────────────────────────────────────────────

class GatewayVehicleListView(APIView):
    """
    Endpoint de Veículos do Gateway.
    """

    @swagger_auto_schema(
        operation_summary="Listar veículos",
        operation_description="Retorna todos os veículos da frota com links HATEOAS.",
        responses={200: openapi.Response(description="Lista de veículos")}
    )
    def get(self, request):
        response = requests.get(f"{VEHICLES_API}/vehicles/")
        vehicles = response.json()

        result = []
        for vehicle in vehicles:
            vehicle['links'] = build_vehicle_links(request, vehicle)
            result.append(vehicle)

        return Response(result, status=response.status_code)

    @swagger_auto_schema(
        operation_summary="Criar veículo",
        operation_description="Cadastra um novo veículo na frota.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['license_plate', 'model', 'year', 'cargo_capacity_kg'],
            properties={
                'license_plate': openapi.Schema(type=openapi.TYPE_STRING, description='Placa do veículo'),
                'model': openapi.Schema(type=openapi.TYPE_STRING, description='Modelo do veículo'),
                'year': openapi.Schema(type=openapi.TYPE_INTEGER, description='Ano de fabricação'),
                'cargo_capacity_kg': openapi.Schema(type=openapi.TYPE_NUMBER, description='Capacidade de carga em kg'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status: available, in_use, maintenance'),
                'driver': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID do motorista (opcional)'),
            }
        ),
        responses={201: openapi.Response(description="Veículo criado")}
    )
    def post(self, request):
        response = requests.post(
            f"{VEHICLES_API}/vehicles/",
            json=request.data
        )
        vehicle = response.json()
        if response.status_code == 201:
            vehicle['links'] = build_vehicle_links(request, vehicle)
        return Response(vehicle, status=response.status_code)


class GatewayVehicleDetailView(APIView):
    """
    Detalhes, atualização e remoção de um veículo específico.
    """

    @swagger_auto_schema(
        operation_summary="Detalhar veículo",
        operation_description="Retorna os dados de um veículo específico com links HATEOAS.",
        responses={
            200: openapi.Response(description="Dados do veículo"),
            404: openapi.Response(description="Veículo não encontrado")
        }
    )
    def get(self, request, pk):
        response = requests.get(f"{VEHICLES_API}/vehicles/{pk}/")
        if response.status_code == 404:
            return Response({'error': 'Veículo não encontrado.'}, status=404)

        vehicle = response.json()
        vehicle['links'] = build_vehicle_links(request, vehicle)
        return Response(vehicle)

    @swagger_auto_schema(
        operation_summary="Atualizar veículo",
        operation_description="Atualiza os dados de um veículo.",
        responses={200: openapi.Response(description="Veículo atualizado")}
    )
    def put(self, request, pk):
        response = requests.put(
            f"{VEHICLES_API}/vehicles/{pk}/",
            json=request.data
        )
        vehicle = response.json()
        if response.status_code == 200:
            vehicle['links'] = build_vehicle_links(request, vehicle)
        return Response(vehicle, status=response.status_code)

    @swagger_auto_schema(
        operation_summary="Remover veículo",
        operation_description="Remove um veículo da frota.",
        responses={204: openapi.Response(description="Veículo removido")}
    )
    def delete(self, request, pk):
        response = requests.delete(f"{VEHICLES_API}/vehicles/{pk}/")
        return Response(status=response.status_code)


# ─── GATEWAY: DRIVERS ───────────────────────────────────────────────────────

class GatewayDriverListView(APIView):
    """
    Endpoint de Motoristas do Gateway.
    """

    @swagger_auto_schema(
        operation_summary="Listar motoristas",
        operation_description="Retorna todos os motoristas cadastrados com links HATEOAS.",
        responses={200: openapi.Response(description="Lista de motoristas")}
    )
    def get(self, request):
        response = requests.get(f"{VEHICLES_API}/drivers/")
        drivers = response.json()

        for driver in drivers:
            driver['links'] = {
                'self': request.build_absolute_uri(f'/gateway/drivers/{driver["id"]}/'),
            }

        return Response(drivers, status=response.status_code)

    @swagger_auto_schema(
        operation_summary="Criar motorista",
        operation_description="Cadastra um novo motorista.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'license_number', 'phone'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Nome completo'),
                'license_number': openapi.Schema(type=openapi.TYPE_STRING, description='Número da CNH'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Telefone de contato'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status: available, on_route, unavailable'),
            }
        ),
        responses={201: openapi.Response(description="Motorista criado")}
    )
    def post(self, request):
        response = requests.post(
            f"{VEHICLES_API}/drivers/",
            json=request.data
        )
        driver = response.json()
        if response.status_code == 201:
            driver['links'] = {
                'self': request.build_absolute_uri(f'/gateway/drivers/{driver["id"]}/'),
            }
        return Response(driver, status=response.status_code)


class GatewayDriverDetailView(APIView):
    """
    Detalhes, atualização e remoção de um motorista específico.
    """

    @swagger_auto_schema(
        operation_summary="Detalhar motorista",
        operation_description="Retorna os dados de um motorista específico com links HATEOAS.",
        responses={
            200: openapi.Response(description="Dados do motorista"),
            404: openapi.Response(description="Motorista não encontrado")
        }
    )
    def get(self, request, pk):
        response = requests.get(f"{VEHICLES_API}/drivers/{pk}/")
        if response.status_code == 404:
            return Response({'error': 'Motorista não encontrado.'}, status=404)

        driver = response.json()
        driver['links'] = {
            'self': request.build_absolute_uri(f'/gateway/drivers/{pk}/'),
            'vehicles': request.build_absolute_uri('/gateway/vehicles/'),
        }
        return Response(driver)

    @swagger_auto_schema(
        operation_summary="Atualizar motorista",
        operation_description="Atualiza os dados de um motorista.",
        responses={200: openapi.Response(description="Motorista atualizado")}
    )
    def put(self, request, pk):
        response = requests.put(
            f"{VEHICLES_API}/drivers/{pk}/",
            json=request.data
        )
        driver = response.json()
        if response.status_code == 200:
            driver['links'] = {
                'self': request.build_absolute_uri(f'/gateway/drivers/{pk}/'),
            }
        return Response(driver, status=response.status_code)

    @swagger_auto_schema(
        operation_summary="Remover motorista",
        operation_description="Remove um motorista do sistema.",
        responses={204: openapi.Response(description="Motorista removido")}
    )
    def delete(self, request, pk):
        response = requests.delete(f"{VEHICLES_API}/drivers/{pk}/")
        return Response(status=response.status_code)
