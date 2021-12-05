from django.contrib import admin
from .models import TransportationCarriageLog, TransportationLog, CarriagePhoto
from django.utils.html import format_html
from operators.admin_forms import GroupPlateAdminForm


@admin.register(TransportationCarriageLog)
class CarriageAdmin(admin.ModelAdmin):
    list_display = ['carriage_number', 'carriage_number']

    def carriage_photo_image(self, obj):
        carriage = CarriagePhoto.objects.filter(carriage=obj.id).first()
        return format_html('<img src="{}" />'.format(carriage.carriage_photo.thumbnail.url))

    def quality_photo_image(self, obj):
        carriage = CarriagePhoto.objects.filter(carriage=obj.id).first()
        return format_html('<img src="{}" />'.format(carriage.carriage_quality_photo.thumbnail.url))

    carriage_photo_image.short_description = 'Распознование номера вагона'
    quality_photo_image.short_description = 'Контроль качества сырья'
    readonly_fields = ['carriage_photo_image', 'quality_photo_image']


class GroupPlatesApiNamesInlineAdmin(admin.TabularInline):
    model = TransportationCarriageLog
    form = GroupPlateAdminForm
    min_num = 1
    extra = 0


@admin.register(TransportationLog)
class TransportationAdmin(admin.ModelAdmin):
    fields = ('name_organization', 'train_number', 'date')

    inlines = [GroupPlatesApiNamesInlineAdmin]


@admin.register(CarriagePhoto)
class CarriagePhotonAdmin(admin.ModelAdmin):
    list_display = ['carriage']

    def carriage_photo_image(self, obj):
        return format_html('<img src="{}" />'.format(obj.carriage_photo.thumbnail.url))

    def quality_photo_image(self, obj):
        return format_html('<img src="{}" />'.format(obj.carriage_quality_photo.thumbnail.url))

    carriage_photo_image.short_description = 'Распознование номера вагона'
    quality_photo_image.short_description = 'Контроль качества сырья'
    readonly_fields = ['carriage_photo_image', 'quality_photo_image']
