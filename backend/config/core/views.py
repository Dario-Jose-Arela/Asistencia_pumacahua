from django.http import JsonResponse
from django.shortcuts import render
from datetime import date
from .models import Estudiante, Asistencia, Horario


def scanner_view(request):
    return render(request, 'scanner.html')

def registrar_asistencia(request):
    try:
        qr_data = request.GET.get('qr')

        if not qr_data:
            return JsonResponse({'error': 'No se recibió QR'})

        # Extraer ID
        partes = qr_data.split('-')
        if len(partes) != 2:
            return JsonResponse({'error': 'Formato de QR inválido'})

        estudiante_id = int(partes[1])

        estudiante = Estudiante.objects.get(id=estudiante_id)

        hoy = date.today()

        # Validar duplicado
        if Asistencia.objects.filter(estudiante=estudiante, fecha=hoy).exists():
            return JsonResponse({'mensaje': 'Ya registraste asistencia hoy'})

        horario = Horario.objects.first()

        if not horario:
            return JsonResponse({'error': 'No hay horarios registrados'})

        Asistencia.objects.create(
            estudiante=estudiante,
            horario=horario,
            estado='PRESENTE'
        )

        return JsonResponse({'mensaje': 'Asistencia registrada correctamente'})

    except Estudiante.DoesNotExist:
        return JsonResponse({'error': 'Estudiante no existe'})

    except Exception as e:
        return JsonResponse({'error': str(e)})