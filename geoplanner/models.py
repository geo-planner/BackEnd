from django.db import models   
from django.contrib.auth.models import User
class RouteType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name 
    

class VehicleType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class RouteStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Depot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    job_code = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    service_time_minutes = models.IntegerField(null=True, blank=True)
    demand = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    starting_time = models.TimeField()
    working_time_minutes = models.IntegerField()

    def __str__(self):
        return self.name
    
class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    route_type = models.ForeignKey(RouteType, on_delete=models.CASCADE)
    route_status = models.ForeignKey(RouteStatus, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    total_distance_km = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    sequence = models.IntegerField()

    def __str__(self):
        return f"{self.route} - stop {self.sequence}"