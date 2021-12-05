from django.urls import path
from operators.views import TransportationView, CarriageView, TestModelView

urlpatterns = [

    path('transportationlog/', TransportationView.as_view()),
    path('trains/', TransportationView.as_view()),
    path('test/', TestModelView.as_view({'post': 'create'})),
    path('carriages/', CarriageView.as_view()),
]