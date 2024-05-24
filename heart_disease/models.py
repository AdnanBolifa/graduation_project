from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, default='')
    age = models.PositiveIntegerField(default=0)
    is_doctor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, default='')
    address = models.TextField(default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

class PatientHistory(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    sex = models.IntegerField(null=True, default=None, blank=True)
    age = models.IntegerField(null=True, default=None, blank=True)
    currentSmoker = models.IntegerField(null=True, default=None, blank=True)
    cigsPerDay = models.IntegerField(null=True, default=None, blank=True)
    BPMeds = models.IntegerField(null=True, default=None, blank=True)
    prevalentStroke = models.IntegerField(null=True, default=None, blank=True)
    prevalentHyp = models.IntegerField(null=True, default=None, blank=True)
    diabetes = models.IntegerField(null=True, default=None, blank=True)
    totChol = models.IntegerField(null=True, default=None, blank=True)
    sysBP = models.IntegerField(null=True, default=None, blank=True)
    diaBP = models.IntegerField(null=True, default=None, blank=True)
    BMI = models.FloatField(null=True, default=None, blank=True)
    heartRate = models.IntegerField(null=True, default=None, blank=True)
    glucose = models.IntegerField(null=True, default=None, blank=True)
    TenYearCHD = models.IntegerField(null=True, default=None, blank=True)
    doctor_feedback = models.BooleanField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
