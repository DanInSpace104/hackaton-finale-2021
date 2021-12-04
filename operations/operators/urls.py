from django.urls import path
from operators.views import TransportationView, CarriageView, test_post_request

urlpatterns = [
    path('transportationlog/', TransportationView.as_view()),
    path('trains/', TransportationView.as_view()),
    path('test/', test_post_request),
    path('carriages/', CarriageView.as_view()),
]