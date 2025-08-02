from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [('doctor', 'Doctor'), ('patient', 'Patient')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    specialization = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.PositiveBigIntegerField(null=True, blank=True)
    available = models.BooleanField(default=False)

    blood_group = models.CharField(max_length=5, null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}  ({self.role})"
    

class Appointment(models.Model):
    STATUS_CHOICE = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected')
    ]

    patient = models.ForeignKey(
        User,
        related_name='appointments_as_patient',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )
    doctor = models.ForeignKey(
        User,
        related_name='appointments_as_doctor',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(default=timezone.now)
    symptoms = models.TextField(null=True, blank=True)
    report = models.FileField(upload_to='reports/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    prescription = models.TextField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.username} with {self.doctor.username} at {self.scheduled_for}"
