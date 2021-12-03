from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import TransportationLog, TransportationCarriageLog
from rest_framework.generics import ListAPIView, ListCreateAPIView
from operators.serializers import TransportationLogSerializer, CarriageSerializer
import rest_framework.generics as generics
from rest_framework.response import Response
from rest_framework import status


class TransportationView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = TransportationLogSerializer
    queryset = TransportationLog.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data
        return Response(response_data, status=status.HTTP_201_CREATED)


class CarriageView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = CarriageSerializer
    queryset = TransportationCarriageLog.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data
        return Response(response_data, status=status.HTTP_201_CREATED)

# class CargoQualityAssesmentView(ListCreateAPIView):
#     serializer_class = CarriageSerializer
#     queryset = CargoQualityAssessment.objects.all()
