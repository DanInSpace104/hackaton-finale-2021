from model_utils.models import TimeStampedModel
# Create your models here.
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user
from model_utils.models import TimeStampedModel


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
    name = models.CharField(max_length=225, verbose_name="Имя компании")
    train_number = models.CharField(max_length=255, unique=True, verbose_name="Номера поезда")
    date = models.DateField(blank=True, null=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Лог транспартировки'
        ordering = ['date']


class TransportationCarriageLog(CreatedUpdatedBy):
    train = models.ForeignKey('operators.TransportationLog', blank=True, null=True, on_delete=models.CASCADE,
                              related_name='train',
                              verbose_name='Поезд')
    cargo_weight = models.CharField(max_length=225, verbose_name="Вес груза")
    carriage_number = models.CharField(max_length=255, unique=True, verbose_name="Номер состава")
    carriage_type = models.CharField(max_length=255, unique=True, verbose_name="Тип вагона")
    carriage_photo = models.ImageField(upload_to='carriage', height_field=100, width_field=100)

    class Meta:
        verbose_name = 'Лог записи вагонов'


class CargoQualityAssessment(CreatedUpdatedBy):
    carriage = models.ForeignKey('operators.TransportationCarriageLog', blank=True, null=True,
                                 on_delete=models.CASCADE,
                                 related_name='carriage',
                                 verbose_name='Вагон')
    quality_control = models.IntegerField(verbose_name="Качество груза")
    carriage_photo = models.ImageField(upload_to='carriage_quality', height_field=100, width_field=100)

    class Meta:
        verbose_name = 'Контроль качества вагонов'
