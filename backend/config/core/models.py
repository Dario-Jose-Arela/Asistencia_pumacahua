from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# ROLES DE USUARIO
# -----------------------------
class Perfil(models.Model):
    ROLES = (
        ('DIRECTOR', 'Director'),
        ('DOCENTE', 'Docente'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"


# -----------------------------
# DOCENTE
# -----------------------------
class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# -----------------------------
# CURSO
# -----------------------------
class Curso(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


# -----------------------------
# SECCION
# -----------------------------
class Seccion(models.Model):
    nombre = models.CharField(max_length=5)  # A, B, C
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.curso.nombre} - {self.nombre}"


# -----------------------------
# ESTUDIANTE
# -----------------------------
import qrcode
from io import BytesIO
from django.core.files import File

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    foto = models.ImageField(upload_to='estudiantes/', null=True, blank=True)
    codigo_qr = models.ImageField(upload_to='qr/', null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Generar QR con el ID del estudiante
        qr_data = f"EST-{self.id}"

        qr_img = qrcode.make(qr_data)

        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')

        filename = f"estudiante_{self.id}.png"

        self.codigo_qr.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)

# -----------------------------
# HORARIO
# -----------------------------
class Horario(models.Model):
    DIAS = (
        ('LUNES', 'Lunes'),
        ('MARTES', 'Martes'),
        ('MIERCOLES', 'Miércoles'),
        ('JUEVES', 'Jueves'),
        ('VIERNES', 'Viernes'),
    )

    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.docente} - {self.seccion} ({self.dia_semana})"


# -----------------------------
# ASISTENCIA
# -----------------------------
class Asistencia(models.Model):
    ESTADOS = (
        ('PRESENTE', 'Presente'),
        ('TARDE', 'Tarde'),
        ('FALTA', 'Falta'),
    )

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS)
    registrado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.estado} - {self.fecha}"