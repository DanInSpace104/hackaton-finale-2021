from django.contrib import admin
from .models import TransportationCarriageLog, TransportationLog, CargoQualityAssessment
from django.utils.html import mark_safe
from django.utils.html import format_html
from operators.admin_forms import GroupPlateAdminForm, CargoQualityAdminForm


@admin.register(TransportationCarriageLog)
class CarriageAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.carriage_photo.url))

    image_tag.short_description = 'Image'
    readonly_fields = ['image_tag']


@admin.register(CargoQualityAssessment)
class ModelCargoAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.carriage_photo.url))

    image_tag.short_description = 'Image'
    readonly_fields = ['image_tag']


class GroupPlatesApiNamesInlineAdmin(admin.TabularInline):
    model = TransportationCarriageLog
    form = GroupPlateAdminForm
    min_num = 1
    extra = 0


class NewAdmin(admin.TabularInline):
    model = CargoQualityAssessment
    form = CargoQualityAssessment
    min_num = 1
    extra = 0


@admin.register(TransportationLog)
class TransportationAdmin(admin.ModelAdmin):
    fields = ('name', 'train_number', 'date')

    inlines = [GroupPlatesApiNamesInlineAdmin]







# @admin.register(CargoQualityAssessment)
# class CargoQualityAssessmentAdmin(admin.ModelAdmin):
#     fields = ('carriage', 'quality_control', 'carriage_photo')
