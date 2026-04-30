"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Fleet Management API Gateway",
        default_version='v1',
        description=(
            "API Gateway para o sistema de gerenciamento de frotas e logística.\n\n"
            "## Arquitetura\n"
            "Este gateway centraliza o acesso aos serviços internos:\n"
            "- **Vehicles Service**: gerencia veículos e motoristas\n"
            "- **Deliveries Service**: gerencia entregas e rastreamento\n\n"
            "## HATEOAS\n"
            "Todas as respostas incluem um campo `links` com as ações disponíveis "
            "para o estado atual do recurso."
        ),
        contact=openapi.Contact(email="contato@fleetmanagement.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[path('gateway/', include('gateway.urls'))],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vehicles/', include('vehicles.urls')),
    path('api/deliveries/', include('deliveries.urls')),
    path('gateway/', include('gateway.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
