from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from usuarios.models import Patient
from nutriFoco.models import BaseModel

User = settings.AUTH_USER_MODEL


class Availability(BaseModel):
    nutritionist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')

    weekday = models.IntegerField()  # 0 = segunda
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.nutritionist} - {self.weekday}"


class Appointment(BaseModel):
    STATUS_CHOICES = (
        ('scheduled', 'Agendada'),
        ('confirmed', 'Confirmada'),
        ('canceled', 'Cancelada'),
        ('done', 'Realizada'),
        ('missed', 'Não compareceu'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    nutritionist = models.ForeignKey(User, on_delete=models.CASCADE)

    datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    notes = models.TextField(blank=True, null=True)

    def clean(self):
        if Appointment.objects.filter(
            nutritionist=self.nutritionist,
            datetime=self.datetime,
            deleted_at__isnull=True
        ).exclude(id=self.id).exists():
            raise ValidationError("Horário já ocupado")

    def __str__(self):
        return f"{self.patient} - {self.datetime}"