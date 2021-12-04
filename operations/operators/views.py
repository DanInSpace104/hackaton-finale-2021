import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import TransportationLog, TransportationCarriageLog
from rest_framework.generics import ListAPIView, ListCreateAPIView
from operators.serializers import TransportationLogSerializer, CarriageSerializer, TestSerializer
import rest_framework.generics as generics
from rest_framework.response import Response
from rest_framework import status
import base64
import os
from django.core.files import File
from rest_framework.views import APIView


from django import forms


def handle_uploaded_file(name, f):
    with open('media'+'name', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=200)
    file = forms.FileField()


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
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     handle_uploaded_file(name=request.FILES['carriage_photo'].name, f=request.FILES['carriage_photo'])
        #     return Response({}, status=status.HTTP_201_CREATED)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response_data = serializer.validated_data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestView(APIView):
    serializer_class = CarriageSerializer
    queryset = TransportationCarriageLog.objects.all()

    def post(self,request,format=None):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            # access the data as serializer.validated_data['keys']
            # save the MyPhoto obj lets call it myphoto
            # get the base64 string
            imgstr64 = serializer.validated_data['corresponding filed in the serializer']
            imgdata = base64.b64decode(imgstr64)
            fname = '/tmp/%s.jpg'%(str(time.time()))
            with open(fname,'wb') as f:
                f.write(imgdata)
            imgname = '%s.jpg'%(str(time.time()))
            myphoto.image.save(imgname, File(open(fname, 'r')))
            os.remove(fname)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_post_request(request):
    print(request)
    print(dict(request.POST.lists()))
    return HttpResponse(status=204)
# class CargoQualityAssesmentView(ListCreateAPIView):
#     serializer_class = CarriageSerializer
#     queryset = CargoQualityAssessment.objects.all()
