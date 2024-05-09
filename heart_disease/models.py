from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class PatientHistory(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    age = models.IntegerField()
    sex = models.IntegerField()
    cp = models.IntegerField()
    trestbps = models.IntegerField()
    chol = models.IntegerField()
    fbs = models.IntegerField()
    restecg = models.IntegerField()
    thalach = models.IntegerField()
    exang = models.IntegerField()
    oldpeak = models.FloatField()
    slope = models.IntegerField()
    ca = models.IntegerField()
    thal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

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
