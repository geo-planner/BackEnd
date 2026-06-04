from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Depot, Job, Vehicle, RouteType, VehicleType, RouteStatus


class RegisterSerializer(serializers.ModelSerializer):
    # pole password2 istnieje tylko do walidacji - nie ma go w modelu User
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        # sprawdzamy czy oba hasla sa identyczne
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Hasla nie sa identyczne.")
        return data

    def create(self, validated_data):
        # usuwamy password2 bo User go nie zna
        validated_data.pop('password2')
        # create_user uzywa wbudowanej metody Django ktora hashuje haslo
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class RouteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteType
        fields = ['id', 'name']


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'name']


class RouteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStatus
        fields = ['id', 'name']


class DepotSerializer(serializers.ModelSerializer):
    # user jest tylko do odczytu — przypisujemy go automatycznie w widoku
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Depot
        fields = ['id', 'user', 'name', 'address', 'latitude', 'longitude', 'created_at']


class JobSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'user', 'address', 'job_code', 'latitude', 'longitude',
                  'service_time_minutes', 'demand', 'created_at']


class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # vehicle_type_name pokazuje nazwe typu zamiast samego ID — czytelniejszy JSON
    vehicle_type_name = serializers.CharField(source='vehicle_type.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'user', 'vehicle_type', 'vehicle_type_name', 'name',
                  'capacity', 'starting_time', 'working_time_minutes']
