from django.contrib import admin
from .models import TransportationCarriageLog, TransportationLog, CargoQualityAssessment


@admin.register(TransportationLog)
class TransportationAdmin(admin.ModelAdmin):
    fields = ('name', 'train_number', 'date')


@admin.register(TransportationCarriageLog)
class CarriageAdmin(admin.ModelAdmin):
    fields = ('train', 'cargo_weight', 'carriage_number', 'carriage_type', 'carriage_photo')


@admin.register(CargoQualityAssessment)
class CargoQualityAssessmentAdmin(admin.ModelAdmin):
    fields = ('carriage', 'quality_control', 'carriage_photo')
