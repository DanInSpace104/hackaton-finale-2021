from .models import TransportationLog, TransportationCarriageLog, CarriagePhoto
from operators.serializers import TransportationLogSerializer, CarriageSerializer, CarriagePhotoSerializer
import rest_framework.generics as generics
from rest_framework.response import Response
from rest_framework import status
from settings.settings import MEDIA_ROOT
from rest_framework import viewsets


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
        serializer.save()
        return Response(response_data, status=status.HTTP_201_CREATED)


class CarriageView(generics.CreateAPIView):
    serializer_class = CarriageSerializer
    queryset = TransportationCarriageLog.objects.all()

    def post(self, request, *args, **kwargs):
        up_file = request.FILES['carriage_photo']
        request.data.pop('carriage_photo')
        carriage_photo_url = MEDIA_ROOT + '/carriage/' + up_file.name
        destination = open(carriage_photo_url, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()
        up_file = request.FILES['carriage_quality_photo']
        request.data.pop('carriage_quality_photo')
        carriage_quality_photo_url = MEDIA_ROOT+'/carriage_quality/' + up_file.name
        destination = open(carriage_quality_photo_url, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response_data = serializer.validated_data
            instance = serializer.save()
            instance.carriage_photo.url = carriage_photo_url
            instance.carriage_quality_photo.url = carriage_quality_photo_url
            instance.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestModelView(viewsets.ModelViewSet):
    serializer_class = CarriagePhotoSerializer
    queryset = CarriagePhoto.objects.all()
    lookup_field = 'carriage_photo'
