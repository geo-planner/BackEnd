from django.contrib import admin
from .models import RouteType, VehicleType, RouteStatus, Depot, Job, Vehicle, Route, RouteStop
# Register your models here.
# przykłady - do dopracowania jak będziemy mieć więcej danych do wyświetlenia
admin.site.register(RouteType)
admin.site.register(RouteStatus)
admin.site.register(Depot)
@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['job_code', 'address', 'user', 'demand','created_at']
    list_filter = ['user']
    search_fields = ['address', 'job_code']

admin.site.register(Vehicle)
admin.site.register(Route)
admin.site.register(RouteStop)