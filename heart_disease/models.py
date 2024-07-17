from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=10, default='', blank=True)
    age = models.PositiveIntegerField(default=0, blank=True)
    is_doctor = models.BooleanField(default=False, blank=True)
    phone_number = models.CharField(max_length=15, default='', blank=True)
    address = models.TextField(default='', blank=True)

    def __str__(self):
        return self.email


class PatientHistory(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    patientName = models.CharField(max_length=50, null=True, default=None, blank=True)
    prediction_type = models.CharField(max_length=50, null=True, default=None, blank=True)
    sex = models.IntegerField(null=True, default=None, blank=True)
    age = models.IntegerField(null=True, default=None, blank=True)
    BMI = models.FloatField(null=True, default=None, blank=True)
    doctor_feedback = models.BooleanField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Heart disease specific fields
    currentSmoker = models.IntegerField(null=True, default=None, blank=True)
    cigsPerDay = models.IntegerField(null=True, default=None, blank=True)
    BPMeds = models.IntegerField(null=True, default=None, blank=True)
    prevalentStroke = models.IntegerField(null=True, default=None, blank=True)
    prevalentHyp = models.IntegerField(null=True, default=None, blank=True)
    diabetes = models.IntegerField(null=True, default=None, blank=True)
    totChol = models.IntegerField(null=True, default=None, blank=True)
    sysBP = models.IntegerField(null=True, default=None, blank=True)
    diaBP = models.IntegerField(null=True, default=None, blank=True)
    heartRate = models.IntegerField(null=True, default=None, blank=True)
    glucose = models.IntegerField(null=True, default=None, blank=True)
    # Diabetes VIP specific fields
    Urea = models.FloatField(null=True, default=None, blank=True)
    Cr = models.FloatField(null=True, default=None, blank=True)
    HbA1c = models.FloatField(null=True, default=None, blank=True)
    Chol = models.FloatField(null=True, default=None, blank=True)
    TG = models.FloatField(null=True, default=None, blank=True)
    HDL = models.FloatField(null=True, default=None, blank=True)
    LDL = models.FloatField(null=True, default=None, blank=True)
    VLDL = models.FloatField(null=True, default=None, blank=True)
    # Diabetes specific fields
    Pregnancies = models.IntegerField(null=True, default=None, blank=True)
    BloodPressure = models.IntegerField(null=True, default=None, blank=True)
    SkinThickness = models.IntegerField(null=True, default=None, blank=True)
    Insulin = models.IntegerField(null=True, default=None, blank=True)
    DiabetesPedigreeFunction = models.FloatField(null=True, default=None, blank=True)
    # Hypertension specific fields
    # same as heart
    Prediction = models.FloatField(null=True, default=None, blank=True)