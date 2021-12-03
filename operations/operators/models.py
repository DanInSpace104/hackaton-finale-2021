from model_utils.models import TimeStampedModel
# Create your models here.
from django.conf import settings
from stdimage import StdImageField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user
from model_utils.models import TimeStampedModel
import os
import uuid
from PIL import Image
from django.db import models


class CreatedUpdatedBy(TimeStampedModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                   null=True, on_delete=models.CASCADE,
                                   related_name='created_%(app_label)s_%(class)s_set',
                                   editable=False,
                                   verbose_name=_('Автор'))
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                    null=True, on_delete=models.CASCADE,
                                    related_name='modified_%(app_label)s_%(class)s_set',
                                    editable=False,
                                    verbose_name=_('Изменил'))

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            self.modified_by = get_current_authenticated_user()
        except ValueError:
            # if anonymous user - don't fill modified_by field
            pass

        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class TransportationLog(CreatedUpdatedBy):
    """ Aggregate all models into single table (automatic update) """
    name_organization = models.CharField(max_length=255, verbose_name="Имя компании")
    train_number = models.CharField(max_length=255, unique=True, verbose_name="Номера поезда")
    date = models.DateField(blank=True, null=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Лог транспортировки'
        ordering = ['date']


class TransportationCarriageLog(CreatedUpdatedBy):
    train = models.ForeignKey('operators.TransportationLog', blank=True, null=True, on_delete=models.CASCADE,
                              related_name='train',
                              verbose_name='Поезд')
    cargo_weight = models.CharField(max_length=255, verbose_name="Вес груза")
    carriage_number = models.CharField(max_length=255, unique=True, verbose_name="Номер состава")
    carriage_type = models.CharField(max_length=255, unique=True, verbose_name="Тип вагона")
    carriage_photo = StdImageField(upload_to='carriage', blank=True,
                                   variations={'thumbnail': (400, 320, True)}, null=True)
    # carriage_photo = models.ImageField(upload_to='carriage', null=True)
    quality_control = models.IntegerField(verbose_name="Качество груза", null=True)
    carriage_quality_photo = StdImageField(upload_to='carriage_quality', blank=True,
                                           variations={'thumbnail': (400, 400, True)}, null=True)

    class Meta:
        verbose_name = 'Вагон '
        verbose_name_plural = 'Лог записи вагонов'


# class CargoQualityAssessment(CreatedUpdatedBy):
#     carriage = models.ForeignKey('operators.TransportationCarriageLog', blank=True, null=True,
#                                  on_delete=models.CASCADE,
#                                  related_name='carriage',
#                                  verbose_name='Вагон')
#     quality_control = models.IntegerField(verbose_name="Качество груза")
#     carriage_photo = models.ImageField(upload_to='carriage_quality')
#
#     class Meta:
#         verbose_name = 'Контроль качества вагонов'
#         verbose_name_plural = 'Контроль качества вагонов'


def upload_to(instance, filename):
    relative_path = instance.url_to_upload.rfind('media/') + len("media/")
    return instance.url_to_upload[relative_path:]
#
#
# class Picture(models.Model):
#     local_url = models.ImageField(upload_to=upload_to)
#     url_to_upload = models.CharField(max_length=200, default='')
#
#     @staticmethod
#     def upload_image(owner, owner_type, picture_type, image, base=""):
#         image_name = Picture.get_uuid_name_with_extension(image)
#         picture = Picture.objects.create(
#             local_url=image,
#             url_to_upload=Uploader.get_path(owner, owner_type, picture_type, image_name, base_for_file=base))
#         return picture
#
#     def delete(self, using=None, keep_parents=False):
#         os.remove(self.url_to_upload)
#         super().delete(using=using, keep_parents=keep_parents)
#
#     @staticmethod
#     def get_uuid_name_with_extension(image):
#         img = Image.open(image)
#         uuid_name = uuid.uuid4()
#         return f'{uuid_name}.{img.format.lower()}'
#



