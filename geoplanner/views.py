import requests
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .serializers import (RegisterSerializer, DepotSerializer, JobSerializer,
                          VehicleSerializer, RouteTypeSerializer, RouteSerializer,
                          VehicleTypeSerializer, RouteStatusSerializer)
from .models import Depot, Job, Vehicle, RouteType, VehicleType, RouteStatus, Route, RouteStop
from .algorithms import solve_tsp


class RegisterView(generics.CreateAPIView):
    # CreateAPIView to gotowy widok DRF do tworzenia obiektow (POST)
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # rejestracja jest publiczna


class GeocodeView(APIView):
    # APIView daje pelna kontrole nad logika — uzywamy gdy nie operujemy bezposrednio na modelu

    def post(self, request):
        addresses = request.data.get('addresses', [])

        if not addresses:
            return Response(
                {'error': 'Podaj liste adresow w polu "addresses".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        for address in addresses:
            # odpytujemy Nominatim — darmowe API OpenStreetMap
            response = requests.get(
                'https://nominatim.openstreetmap.org/search',
                params={'q': address, 'format': 'json', 'limit': 1},
                headers={'User-Agent': 'GeoPlanner/1.0'}  # Nominatim wymaga User-Agent
            )
            data = response.json()

            if data:
                results.append({
                    'address': address,
                    'latitude': float(data[0]['lat']),
                    'longitude': float(data[0]['lon']),
                    'found': True,
                })
            else:
                # jesli nie znaleziono — zwracamy nulls, React moze to wyroznic
                results.append({
                    'address': address,
                    'latitude': None,
                    'longitude': None,
                    'found': False,
                })

        return Response(results, status=status.HTTP_200_OK)


class RouteTypeViewSet(viewsets.ReadOnlyModelViewSet):
    # ReadOnlyModelViewSet — tylko GET /api/route-types/ i GET /api/route-types/{id}/
    queryset = RouteType.objects.all()
    serializer_class = RouteTypeSerializer


class VehicleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer


class RouteStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RouteStatus.objects.all()
    serializer_class = RouteStatusSerializer


class DepotViewSet(viewsets.ModelViewSet):
    serializer_class = DepotSerializer

    def get_queryset(self):
        # zwracamy tylko depotyy nalezace do zalogowanego uzytkownika
        return Depot.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # przy tworzeniu automatycznie przypisujemy zalogowanego uzytkownika
        serializer.save(user=self.request.user)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def solve(self, request, pk=None):
        # detail=True oznacza ze akcja dziala na konkretnym obiekcie: /api/routes/{id}/solve/
        route = self.get_object()

        # pobieramy ID jobow wybranych do tej trasy z body requestu
        job_ids = request.data.get('job_ids', [])
        if not job_ids:
            return Response(
                {'error': 'Podaj liste job_ids do rozwiazania.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # pobieramy joby nalezace do usera (zabezpieczenie przed uzyciem cudzych jobow)
        jobs = Job.objects.filter(id__in=job_ids, user=request.user)

        # sprawdzamy czy wszystkie podane joby maja wspolrzedne
        jobs_without_coords = jobs.filter(latitude=None)
        if jobs_without_coords.exists():
            return Response(
                {'error': 'Niektore joby nie maja wspolrzednych. Najpierw uruchom geocoding.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # przygotowujemy dane dla algorytmu
        depot = route.depot
        depot_point = {'latitude': depot.latitude, 'longitude': depot.longitude}
        job_points = [
            {'id': j.id, 'latitude': j.latitude, 'longitude': j.longitude}
            for j in jobs
        ]

        # uruchamiamy algorytm TSP
        ordered_jobs = solve_tsp(depot_point, job_points)

        # usuwamy stare przystanki jesli trasa byla juz rozwiazywana
        RouteStop.objects.filter(route=route).delete()

        # zapisujemy nowe przystanki z kolejnoscia
        for sequence, job_point in enumerate(ordered_jobs, start=1):
            RouteStop.objects.create(
                route=route,
                job_id=job_point['id'],
                sequence=sequence,
            )

        # zwracamy zaktualizowana trase z przystankami
        serializer = self.get_serializer(route)
        return Response(serializer.data, status=status.HTTP_200_OK)