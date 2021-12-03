from django.urls import path
from operators.views import TransportationView, CarriageView

urlpatterns = [
    path('transportationlog/', TransportationView.as_view()),
    # path('trains/', TransportationView.as_view()),
    path('carriages/', CarriageView.as_view()),
]