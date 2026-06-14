from django.contrib import admin
from .models import RouteType, VehicleType, RouteStatus, Depot, Job, Vehicle, Route, RouteStop


# Słowniki
# Dwa sposoby rejestracji: prosty register i dekorator @admin.register
admin.site.register(RouteType)
admin.site.register(RouteStatus)

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


# Depot
@admin.register(Depot)
class DepotAdmin(admin.ModelAdmin):
    list_display = ['name', 'address_with_coords', 'user', 'is_active']
    list_filter = ['is_active', 'user']
    search_fields = ['name', 'address']

    def address_with_coords(self, obj):
        return f"{obj.address} ({obj.latitude}; {obj.longitude})"
    address_with_coords.short_description = 'Address (Lat; Lon)'


# Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['job_code', 'address', 'coordinates', 'user', 'service_time_minutes', 'demand', 'is_active', 'created_at']
    list_filter = ['user', 'is_active']
    search_fields = ['address', 'job_code']

    def coordinates(self, obj):
        if obj.latitude and obj.longitude:
            return f"({obj.latitude}; {obj.longitude})"
        return '—'
    coordinates.short_description = 'Coordinates'


# Vehicle
admin.site.register(Vehicle)


# RouteStop inline (używany wewnątrz Route)
class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 0
    fields = ['sequence', 'job', 'vehicle']
    ordering = ['sequence']


# Route
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'depot', 'route_type', 'route_status', 'total_distance_km', 'stop_count']
    list_filter = ['route_type', 'route_status']
    search_fields = ['name']
    inlines = [RouteStopInline]

    def stop_count(self, obj):
        #zliczanie liczby przystanków w trasie za pomocą relacji odwrotnej (reverse relation) do modelu RouteStop
        return obj.routestop_set.count()
    stop_count.short_description = 'Stops'


# RouteStop
@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['route', 'job', 'sequence']
    list_filter = ['route']