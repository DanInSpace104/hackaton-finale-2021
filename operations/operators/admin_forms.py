import re

from django.forms import ModelForm, ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from . import models


class GroupPlateAdminForm(ModelForm):
    image = forms.FileField(allow_empty_file=True, required=False)
    image_title = forms.CharField(required=False, disabled=True)

    class Meta:
        model = models.TransportationCarriageLog
        fields = '__all__'


class CargoQualityAdminForm(ModelForm):
    image = forms.FileField(allow_empty_file=True, required=False)
    image_title = forms.CharField(required=False, disabled=True)

    class Meta:
        model = models.CargoQualityAssessment
        fields = '__all__'