from django.contrib import admin
from .models import Perfil, Docente, Curso, Seccion, Estudiante, Horario, Asistencia

admin.site.register(Perfil)
admin.site.register(Docente)
admin.site.register(Curso)
admin.site.register(Seccion)
admin.site.register(Estudiante)
admin.site.register(Horario)
admin.site.register(Asistencia)