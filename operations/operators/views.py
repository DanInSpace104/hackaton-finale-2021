from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import TransportationLog, TransportationCarriageLog, CargoQualityAssessment
from rest_framework.generics import ListAPIView, ListCreateAPIView
from operations.operators.serializers import TransportationLogSerializer, CarriageSerializer, CargoQualityAssessment


class TransportationView(ListCreateAPIView):
    serializer_class = TransportationLogSerializer
    queryset = TransportationLog.objects.all()


class CarriageView(ListCreateAPIView):
    serializer_class = CarriageSerializer
    queryset = TransportationCarriageLog.objects.all()


class CargoQualityAssesmentView(ListCreateAPIView):
    serializer_class = CarriageSerializer
    queryset = CargoQualityAssessment.objects.all()
