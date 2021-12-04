from operators.models import TransportationLog, TransportationCarriageLog
from rest_framework import serializers


class TransportationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationLog
        fields = '__all__'
        extra_fields = []


class CarriageSerializer(serializers.ModelSerializer):
    # carriage_photo = serializers.ImageField(upload_to='carriage',
    #                                         max_length=None, use_url=False)
    # carriage_quality_photo = serializers.ImageField(upload_to='carriage_quality',
    #                                                 max_length=None, use_url=False)

    class Meta:
        model = TransportationCarriageLog
        fields = '__all__'
        extra_fields = []


class TestSerializer(serializers.Serializer):
    # carriage_photo = serializers.ImageField(upload_to='carriage',
    #                                         max_length=None, use_url=False)
    # carriage_quality_photo = serializers.ImageField(upload_to='carriage_quality',
    #                                                 max_length=None, use_url=False)

    class Meta:
        model = TransportationCarriageLog
        fields = '__all__'
        extra_fields = []


# class CargoQualityAssessmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CargoQualityAssessment
#         fields = '__all__'
#         extra_fields = []
