from django.urls import path
from .views import HeartDiseasePredict

urlpatterns = [
    path('predict/', HeartDiseasePredict.as_view(), name='heart_disease_predict'),
]
