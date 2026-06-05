from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (RegisterView, GeocodeView, DepotViewSet, JobViewSet,
                    VehicleViewSet, RouteTypeViewSet, VehicleTypeViewSet,
                    RouteStatusViewSet, RouteViewSet)

router = DefaultRouter()
# slowniki - read only
router.register(r'route-types', RouteTypeViewSet, basename='routetype')
router.register(r'vehicle-types', VehicleTypeViewSet, basename='vehicletype')
router.register(r'route-statuses', RouteStatusViewSet, basename='routestatus')
# glowne zasoby
router.register(r'depots', DepotViewSet, basename='depot')
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'routes', RouteViewSet, basename='route')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('geocode/', GeocodeView.as_view(), name='geocode'),
]