from operators.models import TransportationLog, TransportationCarriageLog, CarriagePhoto
from rest_framework import serializers


class TransportationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationLog
        fields = '__all__'
        extra_fields = []


class CarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationCarriageLog
        fields = '__all__'
        extra_fields = []


class CarriagePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarriagePhoto
        fields = '__all__'
        extra_fields = []
