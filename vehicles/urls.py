from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, VehicleViewSet

router = DefaultRouter()
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')

urlpatterns = router.urls
