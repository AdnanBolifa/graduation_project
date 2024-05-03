from django.db import models

class HeartDisease(models.Model):
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

    def __str__(self):
        return str(self.pk)
