from django.urls import path
from .views import registrar_asistencia
from .views import scanner_view

urlpatterns = [
    path('scan/', registrar_asistencia),
    path('scanner/', scanner_view),
]
