from operations.operators.models import TransportationLog, TransportationCarriageLog, CargoQualityAssessment
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


class CargoQualityAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoQualityAssessment
        fields = '__all__'
        extra_fields = []
