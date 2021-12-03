import re

from django.forms import ModelForm, ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from . import models


class GroupPlateAdminForm(ModelForm):
    class Meta:
        model = models.TransportationCarriageLog
        fields = '__all__'


class CargoQualityAdminForm(ModelForm):
    class Meta:
        model = models.CargoQualityAssessment
        fields = '__all__'